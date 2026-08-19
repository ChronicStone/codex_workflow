#!/usr/bin/env python3
"""Deterministic codex_workflow lifecycle CLI.

Lifecycle commands validate and apply their mutations directly. The destructive
``remove`` command is the exception: it plans first and applies only with its
hidden confirmation flag. The hidden ``--apply`` option remains accepted for
compatibility with older launchers.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("codex_workflow requires Python 3.11 or newer")

from runtime.config import load_config
from runtime.analyze import analyze_thread
from runtime.errors import WorkflowError
from runtime.layout import PROJECT_ID
from runtime.lifecycle import (
    OperationPlan,
    PackageLayout,
    ProjectPaths,
    RuntimePaths,
    plan_bootstrap,
    plan_auto_check_update_setting,
    plan_configure,
    plan_enable,
    plan_personalize,
    plan_remove,
    plan_update,
)
from runtime.release import (
    acquire,
    parse_semver,
    select_latest,
    select_releases,
    summarize_release_notes,
)


def _default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def _add_common(parser: argparse.ArgumentParser, *, project: bool = True) -> None:
    parser.add_argument("--codex-home", type=Path, default=_default_codex_home())
    if project:
        parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true", default=True, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="emit compact JSON")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    install = commands.add_parser("install")
    _add_common(install)
    # Retained for callers that have an extracted package available. This is
    # a read-only project-install source; install never bootstraps user files.
    install.add_argument("--package-root", type=Path, help=argparse.SUPPRESS)

    bootstrap = commands.add_parser("bootstrap", help=argparse.SUPPRESS)
    _add_common(bootstrap)
    bootstrap.add_argument(
        "--package-root", type=Path, default=Path(__file__).resolve().parent
    )

    update = commands.add_parser("update")
    _add_common(update, project=False)
    update.add_argument(
        "--project",
        type=Path,
        help="also update a legacy workflow-owned project entry point",
    )
    # Internal hand-off from an installed launcher; not a public prompt form.
    update.add_argument("--source", type=Path, help=argparse.SUPPRESS)
    update.add_argument("--allow-downgrade", action="store_true")
    update.add_argument(
        "--legacy-local-instructions",
        type=Path,
        help="reviewed local instructions extracted from a legacy merged entry point",
    )

    remove = commands.add_parser("remove")
    _add_common(remove)
    remove.add_argument("--confirm", action="store_true", help=argparse.SUPPRESS)

    auto_check = commands.add_parser("auto-check-update")
    _add_common(auto_check, project=False)

    check_update = commands.add_parser("check-update")
    _add_common(check_update, project=False)

    for name in (
        "enable-auto-check-update",
        "disable-auto-check-update",
        # Compatibility aliases retained from releases that called a
        # notification-only check an automatic update.
        "enable-auto-update",
        "disable-auto-update",
    ):
        command = commands.add_parser(name)
        _add_common(command, project=False)

    configure = commands.add_parser("configure")
    _add_common(configure, project=False)
    configure.add_argument(
        "--reasoning-effort",
        choices=["high", "xhigh"],
        help="legacy override that sets implementation and support effort together",
    )
    configure.add_argument("--implementation-effort", choices=["high", "xhigh"])
    configure.add_argument("--support-effort", choices=["high", "xhigh"])
    configure.add_argument("--max-workers", type=int)
    configure.add_argument("--report-size", type=int)
    configure.add_argument(
        "--auto-check-update",
        choices=["enabled", "disabled"],
        help=argparse.SUPPRESS,
    )

    personalize = commands.add_parser("personalize")
    _add_common(personalize)
    personalize.add_argument("--resource", type=Path, required=True)

    for name in ("enable", "disable"):
        command = commands.add_parser(name)
        _add_common(command)

    validate = commands.add_parser("validate")
    _add_common(validate, project=False)
    validate.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parent)

    analyze = commands.add_parser("analyze-thread")
    _add_common(analyze, project=False)
    analyze.add_argument("reference", help="native Codex session ID or rollout JSONL path")
    analyze.add_argument(
        "--sessions-root",
        type=Path,
        help="override the native Codex sessions directory",
    )
    return parser.parse_args()


def _paths(args: argparse.Namespace) -> tuple[RuntimePaths, ProjectPaths | None]:
    runtime = RuntimePaths(args.codex_home.expanduser().resolve())
    project_path = getattr(args, "project", None)
    project = ProjectPaths(project_path.resolve()) if project_path is not None else None
    return runtime, project


def _emit(value: dict[str, object], *, compact: bool) -> None:
    if compact:
        print(json.dumps(value, separators=(",", ":"), sort_keys=True))
    else:
        print(json.dumps(value, indent=2, sort_keys=True))


def _is_workflow_owned_project(project: ProjectPaths) -> bool:
    entries = [path for path in (project.active, project.disabled) if path.is_file()]
    return len(entries) == 1 and PROJECT_ID in entries[0].read_text(encoding="utf-8")


def _finish(plan: OperationPlan, args: argparse.Namespace) -> int:
    summary = plan.summary()
    summary["applied"] = True
    plan.apply()
    _emit(summary, compact=args.json)
    return 0


def _delegate_update(incoming: PackageLayout, args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        "-B",
        str(incoming.root / "workflow.py"),
        "update",
        "--source",
        str(incoming.root),
        "--codex-home",
        str(args.codex_home),
    ]
    if args.project is not None:
        command.extend(["--project", str(args.project)])
    if args.allow_downgrade:
        command.append("--allow-downgrade")
    if args.legacy_local_instructions:
        command.extend(
            ["--legacy-local-instructions", str(args.legacy_local_instructions)]
        )
    if args.apply:
        command.append("--apply")
    if args.json:
        command.append("--json")
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    args = parse_args()
    temporary = None
    try:
        runtime, project = _paths(args)
        if args.command == "analyze-thread":
            sessions_root = (
                args.sessions_root.expanduser().resolve()
                if args.sessions_root is not None
                else runtime.codex_home / "sessions"
            )
            _emit(
                analyze_thread(args.reference, sessions_root=sessions_root),
                compact=args.json,
            )
            return 0
        if args.command == "validate":
            package = PackageLayout.resolve(args.package_root)
            _emit(
                {
                    "valid": True,
                    "version": package.version,
                    "workers": sorted(package.worker_names),
                },
                compact=args.json,
            )
            return 0
        if args.command == "auto-check-update":
            config = load_config(
                runtime.runtime / "workflow_config.json",
                templates=runtime.runtime / "templates" / "agents",
            )
            if not config.auto_check_update:
                _emit(
                    {"status": "disabled", "installed": None, "available": None},
                    compact=args.json,
                )
                return 0
            installed_text = (runtime.runtime / "VERSION").read_text(encoding="utf-8").strip()
            installed = parse_semver(installed_text)
            selected = select_latest()
            status = "current" if selected.version == installed else (
                "update available" if selected.version > installed else "installed newer"
            )
            _emit(
                {
                    "status": status,
                    "installed": installed_text,
                    "available": selected.version_text,
                    "asset": selected.zip_name,
                },
                compact=args.json,
            )
            return 0
        if args.command == "check-update":
            installed_text = (runtime.runtime / "VERSION").read_text(encoding="utf-8").strip()
            installed = parse_semver(installed_text)
            releases = select_releases()
            newer = [release for release in releases if release.version > installed]
            latest = releases[0]
            updates = [
                {
                    "version": release.version_text,
                    "asset": release.zip_name,
                    "release_url": release.release_url,
                    "release_notes": release.release_notes,
                    "summary": summarize_release_notes(release.release_notes),
                }
                for release in newer
            ]
            if newer:
                status = "update available"
                summary = "\n".join(
                    f"{item['version']}: {item['summary']}" for item in updates
                )
            elif latest.version == installed:
                status = "current"
                summary = "The installed workflow is current."
            else:
                status = "installed newer"
                summary = "The installed workflow is newer than the latest release."
            _emit(
                {
                    "status": status,
                    "installed": installed_text,
                    "available": latest.version_text,
                    "asset": latest.zip_name,
                    "summary": summary,
                    "updates": updates,
                },
                compact=args.json,
            )
            return 0
        if args.command == "remove":
            plan = plan_remove(runtime)
            if not args.confirm:
                summary = plan.summary()
                summary["applied"] = False
                summary["confirmation_required"] = True
                _emit(summary, compact=args.json)
                return 0
            return _finish(plan, args)
        if args.command in {
            "enable-auto-check-update",
            "disable-auto-check-update",
            "enable-auto-update",
            "disable-auto-update",
        }:
            return _finish(
                plan_auto_check_update_setting(
                    runtime,
                    enabled=args.command in {
                        "enable-auto-check-update",
                        "enable-auto-update",
                    },
                ),
                args,
            )
        if args.command == "bootstrap":
            package = PackageLayout.resolve(args.package_root)
            return _finish(plan_bootstrap(package, runtime), args)
        if args.command == "install":
            if (runtime.runtime / "VERSION").is_file():
                installed = (runtime.runtime / "VERSION").read_text(encoding="utf-8").strip()
            elif args.package_root is not None:
                raise WorkflowError(
                    "the workflow package is available but the global bootstrap is not installed"
                )
            else:
                raise WorkflowError(
                    "the global workflow bootstrap is not installed"
                )
            _emit(
                {
                    "applied": False,
                    "status": "globally enabled",
                    "version": installed,
                    "instruction": "No per-project installation is required.",
                },
                compact=args.json,
            )
            return 0
        if args.command == "update":
            if args.source:
                incoming = PackageLayout.resolve(args.source)
            else:
                selected = select_latest()
                temporary, package_path = acquire(selected)
                incoming = PackageLayout.resolve(package_path)
            if incoming.root != Path(__file__).resolve().parent:
                return _delegate_update(incoming, args)
            ignored_legacy_project = False
            if args.source is not None and project is not None:
                entries = [
                    path for path in (project.active, project.disabled) if path.exists()
                ]
                if len(entries) <= 1 and not _is_workflow_owned_project(project):
                    project = None
                    ignored_legacy_project = True
            installed_text = (runtime.runtime / "VERSION").read_text(encoding="utf-8").strip()
            if parse_semver(incoming.version) < parse_semver(installed_text) and not args.allow_downgrade:
                raise WorkflowError("incoming version is older; pass --allow-downgrade after approval")
            legacy_local = (
                args.legacy_local_instructions.read_text(encoding="utf-8")
                if args.legacy_local_instructions
                else None
            )
            if legacy_local is not None and project is None:
                raise WorkflowError("--legacy-local-instructions requires --project")
            plan = plan_update(
                incoming,
                runtime,
                project,
                legacy_local_instructions=legacy_local,
            )
            if ignored_legacy_project:
                plan.warnings.append(
                    "ignored a non-workflow-owned project forwarded by an older launcher"
                )
            return _finish(plan, args)
        if args.command == "configure":
            if args.reasoning_effort is not None and (
                args.implementation_effort is not None
                or args.support_effort is not None
            ):
                raise WorkflowError(
                    "--reasoning-effort cannot be combined with role-specific effort flags"
                )
            implementation_effort = (
                args.reasoning_effort
                if args.reasoning_effort is not None
                else args.implementation_effort
            )
            support_effort = (
                args.reasoning_effort
                if args.reasoning_effort is not None
                else args.support_effort
            )
            changes = {
                "default_executor_reasoning_effort": implementation_effort,
                "default_subagent_reasoning_effort": support_effort,
                "max_concurrent_workers": args.max_workers,
                "report_package_size": args.report_size,
                "auto_check_update": (
                    args.auto_check_update == "enabled"
                    if args.auto_check_update is not None
                    else None
                ),
            }
            return _finish(plan_configure(runtime, changes), args)
        if args.command == "personalize":
            assert project is not None
            resource = args.resource.read_text(encoding="utf-8")
            return _finish(plan_personalize(project, resource), args)
        if args.command in {"enable", "disable"}:
            assert project is not None
            return _finish(plan_enable(project, enable=args.command == "enable"), args)
        raise WorkflowError(f"unsupported command: {args.command}")
    except (OSError, WorkflowError) as error:
        _emit({"error": str(error), "applied": False}, compact=getattr(args, "json", False))
        return 1
    finally:
        if temporary is not None:
            temporary.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
