# Medium Route

Use after the Medium route is selected under `AGENTS.md`.

## Main-Agent Role

Perform planning, implementation, verification, and documentation directly.
Do not delegate to worker subagents. Explorer remains available as the
deployment-session companion defined by
`~/.codex/codex_workflow/explorer_companion.md`.

Keep process proportional; simple tasks do not need the full workflow.

## Execution

- Work in bounded stages: context, inspection, implementation, verification,
  and final review.
- Batch independent, known, non-conflicting reads, searches, metadata checks,
  and isolated validation.
- Keep dependent or overlapping edits sequential.
- Run validation concurrently only when commands share no build output,
  generated files, fixtures, databases, ports, devices, or other mutable state.
- Do not create extra stages or commands merely to batch them.

## Plans and Status

When the user says **"plan the implementation for..."** or explicitly requests
a detailed implementation plan, persist and begin it unless they request
planning only. Record:

- Goal, scope, constraints, and acceptance criteria.
- Major steps, dependencies, and protected areas.
- Verification, blockers, and next action.

For durable or multi-session work, update
`agent_docs/project_progress.md` at most twice:

1. Activate the bounded plan.
2. Reconcile final status, evidence, blockers, and next action.

Do not update it after every checkpoint. Keep plan changes traceable.

## Working Rules

- Keep changes focused and preserve unrelated user work.
- Verify in proportion to risk; never claim unrun checks passed.
- Reinspect only after a change, failure, or newly discovered dependency.
- Update durable documentation only for lasting architecture, structure,
  workflow, public behavior, significant decisions, or module usage changes.
- Use verified implementation and tests as documentation sources.
- Update `agent_docs/project_diary.md` only for lasting decisions, discarded
  approaches, or architectural lessons.

For a blocker, record the failed step, evidence, suspected cause, completed
changes and repository state, affected criterion, and required input. Preserve a
clear continuation point and never present partial work as complete.

## Session End

When the user says the exact phrase `end this session`, ignoring capitalization
and surrounding punctuation, follow
`~/.codex/codex_workflow/end_of_session.md` under the Medium branch.
