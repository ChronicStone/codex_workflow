# Medium Route

Use after Medium is selected under `AGENTS.md`.

## Role and Context

You are the main agent.

The main agent performs planning, implementation, verification, and
documentation. Do not delegate those tasks. The only subagents are the single
persistent Explorer defined by `explorer_companion.md` and the fresh
`end_of_session` worker required for an invoked handoff.

Use Explorer as the context gateway: request a planning brief before broad
inspection and focused follow-up briefs for peripheral, unfamiliar, external,
or newly discovered context. The main agent remains responsible for source it
edits, acceptance decisions, critical evidence, and final claims. Inspect
underlying evidence when a brief is uncertain, contradictory, decision-relevant,
or insufficient for safe implementation.

Keep process proportional; small tasks do not require every stage.

## Execution

- Work in bounded context, inspection, implementation, verification, and review
  stages.
- Batch independent, already-known reads, searches, metadata checks, and
  isolated validation. Keep dependent or overlapping edits sequential.
- Run checks concurrently only when they share no mutable build output,
  generated files, fixtures, databases, ports, devices, or processes.
- Keep detailed logs in artifacts and retain only the claim, result, exact
  command or method, artifact path, critical excerpt if needed, and confidence.
- Reinspect after a change, failure, contradiction, or newly discovered
  dependency—not as routine repetition.
- Preserve unrelated work, verify in proportion to risk, and never claim an
  unrun check passed.

## Plans and Durable Status

When the user asks to plan an implementation, persist and begin it unless they
request planning only. Record the goal, major milestones, overall progress,
current position, and next milestone.

For durable or multi-session work, update `agent_docs/project_progress.md` at
most twice: once to activate the bounded plan and once to reconcile its final
state. Use `agent_docs/latest_session_work.md` only for a needed cross-session
handoff, not as scratch space.

Update durable documentation only for lasting architecture, structure,
workflow, public behavior, significant decisions, or module usage. Update
`project_diary.md` only for lasting decisions, discarded approaches, or reusable
architectural lessons.

For a blocker, preserve a clear continuation point and record the failed step,
evidence, suspected cause, completed state, affected criterion, and required
input. Never present partial work as complete.

## Session End

When the user says the exact phrase `end this session`, ignoring capitalization
and surrounding punctuation, follow `~/.codex/codex_workflow/end_of_session.md`.
