# Medium Route

Use after the Medium route is selected under `AGENTS.md`.

## Main-Agent Role

Perform planning, implementation, verification, and documentation directly.
Do not delegate those tasks to workers. Explorer remains available as the
deployment-session companion defined by
`~/.codex/codex_workflow/explorer_companion.md`. The only worker exception is
the fresh `end_of_session` worker required for an invoked handoff.

Keep process proportional; simple tasks do not need the full workflow.

## Stage Execution and Tool Batching
Divide work into bounded stages such as context loading, targeted inspection, implementation, verification, and final review.

At any stage, send focused investigation of peripheral, unfamiliar, or newly discovered context to the existing explorer thread. The assigned focus is a starting point, and the explorer may follow related read-only context when useful. Do not initialize another explorer. Foundational project documents, central implementation surfaces, and decision-critical evidence remain the main agent's direct responsibility.

Before each stage, collect all independent, already-known, non-conflicting tool operations and apply the shared batching rules from AGENTS.md. Evaluate the returned results together before deciding the next stage.

Typical Medium-route batches include:

Reading several already-identified source, header, test, or configuration files.
Searching several known symbols or call sites.
Collecting independent repository metadata.
Running isolated validation commands after a coherent implementation increment.
Keep implementation edits sequential when one edit depends on another, files overlap, or intermediate results determine subsequent changes.

Run validation concurrently only when commands do not share mutable build output, generated files, fixtures, databases, ports, devices, or other state. Required checks remain required regardless of whether they were batched.

Do not manufacture stages or extra commands merely to create a batch. Small tasks may remain a single inspection, edit, and validation sequence.

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

- Goal and major milestones.
- Overall progress and current position.
- Next milestone.

For durable or multi-session work, update
`agent_docs/project_progress.md` at most twice:

1. Activate the bounded plan.
2. Reconcile overall progress, current position, and next milestone.

Do not update it after every checkpoint. Keep detailed current work,
verification, blockers, and the exact continuation point in
`agent_docs/latest_session_work.md` only when a durable handoff is needed.

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
and surrounding punctuation, follow the delegation contract in
`~/.codex/codex_workflow/end_of_session.md`.
