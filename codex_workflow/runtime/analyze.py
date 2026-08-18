"""Read-only analysis of native Codex parent and child rollout records."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from .errors import ValidationError


def _timestamp_ms(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1000)


def _session_meta(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as source:
            for line in source:
                record = json.loads(line)
                if record.get("type") == "session_meta":
                    payload = record.get("payload")
                    if isinstance(payload, dict):
                        return payload
                    break
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"cannot read rollout {path}: {error}") from error
    raise ValidationError(f"rollout has no session metadata: {path}")


def _resolve_rollout(reference: str, sessions_root: Path) -> Path:
    candidate = Path(reference).expanduser()
    if candidate.is_file():
        return candidate.resolve()
    if not sessions_root.is_dir():
        raise ValidationError(f"Codex sessions directory does not exist: {sessions_root}")
    matches = list(sessions_root.rglob(f"*{reference}*.jsonl"))
    exact = []
    for path in matches:
        try:
            if _session_meta(path).get("id") == reference:
                exact.append(path)
        except ValidationError:
            continue
    selected = exact or matches
    if not selected:
        raise ValidationError(
            "no native Codex rollout matches the reference; provide a Codex session "
            "ID or an explicit rollout JSONL path"
        )
    if len(selected) != 1:
        raise ValidationError(f"rollout reference is ambiguous: {reference}")
    return selected[0].resolve()


def _child_rollouts(parent_id: str, sessions_root: Path) -> list[Path]:
    matches: list[Path] = []
    for path in sessions_root.rglob("*.jsonl"):
        try:
            meta = _session_meta(path)
        except ValidationError:
            continue
        source = meta.get("source")
        if not isinstance(source, dict):
            continue
        subagent = source.get("subagent")
        if not isinstance(subagent, dict):
            continue
        spawn = subagent.get("thread_spawn")
        if isinstance(spawn, dict) and spawn.get("parent_thread_id") == parent_id:
            matches.append(path.resolve())
    return sorted(matches)


def _usage() -> dict[str, int]:
    return {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "cache_write_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }


def _analyze_rollout(path: Path) -> tuple[dict[str, Any], list[tuple[int, int]]]:
    meta: dict[str, Any] | None = None
    first_timestamp: str | None = None
    last_timestamp: str | None = None
    models: set[str] = set()
    efforts: set[str] = set()
    completed_turns = 0
    aborted_turns = 0
    active_turn_ms = 0
    model_generations = 0
    context_compactions = 0
    final_usage = _usage()
    tool_calls: Counter[str] = Counter()
    nested_tool_calls: Counter[str] = Counter()
    started_turns: dict[str, int] = {}
    intervals: list[tuple[int, int]] = []

    try:
        with path.open(encoding="utf-8") as source:
            for line in source:
                record = json.loads(line)
                timestamp = record.get("timestamp")
                if isinstance(timestamp, str):
                    first_timestamp = first_timestamp or timestamp
                    last_timestamp = timestamp
                record_type = record.get("type")
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                if record_type == "session_meta":
                    meta = payload
                elif record_type == "turn_context":
                    model = payload.get("model")
                    effort = payload.get("effort")
                    if isinstance(model, str):
                        models.add(model)
                    if isinstance(effort, str):
                        efforts.add(effort)
                elif record_type == "response_item" and payload.get("type") in {
                    "function_call",
                    "custom_tool_call",
                }:
                    name = payload.get("name")
                    if isinstance(name, str):
                        tool_calls[name] += 1
                    tool_input = payload.get("input")
                    if isinstance(tool_input, str):
                        nested_tool_calls.update(
                            re.findall(r"\btools\.([A-Za-z0-9_]+)\s*\(", tool_input)
                        )
                elif record_type == "event_msg":
                    event_type = payload.get("type")
                    if event_type == "task_started":
                        turn_id = payload.get("turn_id")
                        started_at = payload.get("started_at")
                        if isinstance(turn_id, str) and isinstance(started_at, int):
                            started_turns[turn_id] = started_at * 1000
                    elif event_type in {"task_complete", "turn_aborted"}:
                        duration = payload.get("duration_ms")
                        if isinstance(duration, int):
                            active_turn_ms += duration
                        turn_id = payload.get("turn_id")
                        completed_at = payload.get("completed_at")
                        if (
                            isinstance(turn_id, str)
                            and turn_id in started_turns
                            and isinstance(completed_at, int)
                        ):
                            intervals.append(
                                (started_turns.pop(turn_id), completed_at * 1000)
                            )
                        if event_type == "task_complete":
                            completed_turns += 1
                        else:
                            aborted_turns += 1
                    elif event_type == "token_count":
                        model_generations += 1
                        info = payload.get("info")
                        usage = (
                            info.get("total_token_usage")
                            if isinstance(info, dict)
                            else None
                        )
                        if isinstance(usage, dict):
                            final_usage = {
                                key: usage.get(key)
                                if isinstance(usage.get(key), int)
                                else 0
                                for key in _usage()
                            }
                    elif event_type == "context_compacted":
                        context_compactions += 1
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"cannot analyze rollout {path}: {error}") from error

    if meta is None or first_timestamp is None or last_timestamp is None:
        raise ValidationError(f"rollout is incomplete: {path}")
    source = meta.get("source")
    spawn = None
    if isinstance(source, dict):
        subagent = source.get("subagent")
        if isinstance(subagent, dict) and isinstance(
            subagent.get("thread_spawn"), dict
        ):
            spawn = subagent["thread_spawn"]
    started_ms = _timestamp_ms(first_timestamp)
    ended_ms = _timestamp_ms(last_timestamp)
    return (
        {
            "session_id": meta.get("id"),
            "rollout": str(path),
            "agent_path": spawn.get("agent_path") if spawn else None,
            "agent_role": spawn.get("agent_role") if spawn else None,
            "models": sorted(models),
            "reasoning_efforts": sorted(efforts),
            "started_at": first_timestamp,
            "ended_at": last_timestamp,
            "elapsed_ms": ended_ms - started_ms,
            "active_turn_ms": active_turn_ms,
            "completed_turns": completed_turns,
            "aborted_turns": aborted_turns,
            "model_generations": model_generations,
            "context_compactions": context_compactions,
            "tool_calls": dict(tool_calls.most_common()),
            "nested_tool_calls": dict(nested_tool_calls.most_common()),
            "token_usage": final_usage,
        },
        intervals,
    )


def _max_concurrency(intervals: list[tuple[int, int]]) -> int:
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        if end > start:
            events.extend(((start, 1), (end, -1)))
    active = 0
    maximum = 0
    for _, change in sorted(events, key=lambda item: (item[0], item[1])):
        active += change
        maximum = max(maximum, active)
    return maximum


def analyze_thread(reference: str, *, sessions_root: Path) -> dict[str, Any]:
    """Analyze one native Codex parent session and its direct children."""

    parent_path = _resolve_rollout(reference, sessions_root)
    parent, _ = _analyze_rollout(parent_path)
    parent_id = parent.get("session_id")
    if not isinstance(parent_id, str):
        raise ValidationError(f"parent rollout has no session ID: {parent_path}")
    children: list[dict[str, Any]] = []
    child_intervals: list[tuple[int, int]] = []
    for path in _child_rollouts(parent_id, sessions_root):
        child, intervals = _analyze_rollout(path)
        children.append(child)
        child_intervals.extend(intervals)

    totals: dict[str, dict[str, int]] = {}
    for session in [parent, *children]:
        model_names = session["models"]
        model = model_names[0] if len(model_names) == 1 else "mixed"
        aggregate = totals.setdefault(model, {**_usage(), "model_generations": 0})
        for key, value in session["token_usage"].items():
            aggregate[key] += value
        aggregate["model_generations"] += session["model_generations"]

    return {
        "parent": parent,
        "children": children,
        "child_count": len(children),
        "max_child_concurrency": _max_concurrency(child_intervals),
        "totals_by_model": totals,
    }
