# Heavy Route

Use after the Heavy route is selected under `AGENTS.md`.

<!-- codex-workflow-effective-config-start -->
## Effective Workflow Configuration

- Default worker: `executor_luna`.
- Enabled workers: `executor_luna`, `executor_sol`, `tester`, `doc-writer`, `explorer`.
- Maximum concurrent child workers: `5`.
- Maximum `executor_sol` workers: `1`.
- Maximum worker final-report package: `250` words.

Create only enabled workers and obey these limits.
<!-- codex-workflow-effective-config-end -->

## Main-Agent Role

You are the main agent.
The main agent owns:

- Direction, scope, acceptance criteria, plan, and task IDs.
- Package boundaries, dependencies, ownership, and worker coordination.
- Critical review, integration decisions, verification gates, and completion.
- Git state, user communication, `agent_docs/project_progress.md`, and
  `agent_docs/latest_session_work.md`.

Review critical changes and integration boundaries; broaden review only for
high risk, missing evidence, or conflicting results. Worker TOMLs own internal
implementation, testing, batching, and reporting behavior. Do not repeat those
instructions here or in task capsules.

Simple queries do not require delegation.

## Plans and Status

When the user says **"plan the implementation for..."** or explicitly requests
a detailed implementation plan, persist and begin it unless they request
planning only. Record:

- Goal, scope, constraints, and acceptance criteria.
- Ordered tasks, roles, dependencies, and parallel boundaries.
- Verification gates, blockers, and next action.

For durable or multi-session work, update
`agent_docs/project_progress.md` at most twice:

1. Activate the bounded plan.
2. Reconcile final status, evidence, blockers, and next action.

Do not write status for short-lived work or after every checkpoint. Write
`agent_docs/latest_session_work.md` only for a durable cross-session handoff or
`end this session`; replace its content and never use it as scratch space. These
two files remain main-agent owned.

## Delegation

Use the fewest workers needed. Split packages only across independent ownership
and mutable resources.

- `executor_luna`: default production implementation.
- `executor_sol`: when enabled, reserve for core work requiring substantial
  mathematical or logical reasoning, or exceptionally difficult cross-cutting
  work that cannot be narrowed effectively.
- `tester`: independent verification; normally starts after executor self-check,
  unless parallel test research has clear independent value.
- `doc-writer`: after verification, for durable architecture, structure,
  workflow, public behavior, decisions, or usage; never the two status files.
- `explorer`: follow `~/.codex/codex_workflow/explorer_companion.md`; it is a
  companion, not a worker.

Every initial worker capsule must use `fork_turns="none"`, normally stay within
200 words, and never exceed 400 words. Include only:

- Task ID/iteration and bounded outcome.
- Ownership and expected edit surface.
- Context grouped as documents, then source/tests/interfaces/call sites.
- Acceptance criteria and validation.
- Protected areas and return format.
- Optional short advice or suggestions from the main agent for this package.

If work must expand, require evidence and proposed files, resolve overlap, then
send a scoped follow-up. Follow-ups stay within 120 words and contain only task
ID/iteration, changed scope or state, new evidence, affected criterion, useful
updated advice, and next action. Do not resend unchanged context or old logs.

Obey configured worker limits. Run workers concurrently only when ownership and
mutable resources do not conflict; keep lifecycle and repair-loop operations
sequential and evidence-driven.

## Handoff and Verification

1. Executor returns a coherent implementation and focused self-check evidence.
2. Main agent reviews scope, critical changes, and integration boundaries.
3. Tester runs focused and required regression verification.
4. Test/fixture defects stay with tester; production defects return to the same
   executor, then to the same tester.
5. Delegate durable documentation only after relevant behavior is verified.
6. Main agent reconciles final evidence and status.

Rules:

- Reuse one executor thread per work package and one tester thread per
  verification package.
- Reject intent-only or evidence-free checkpoints.
- Do not rerun evidenced checks unless later changes, conflicting evidence, or
  integration risk invalidate them.
- Require meaningful tests for behavior changes, bug fixes, important modules,
  and public contracts.
- Prefer deterministic local fixtures and verification over network dependencies.
- Never weaken validation, claim unrun checks passed, or accept unrelated scope.
- Reject unrelated refactors, hard-coded configurable values, silent error
  suppression, and unplanned public API or schema breaks.

## Failure, Waiting, and Blockers

- After an evidence-free worker response, send one focused retry; replace after
  the second. The replacement must provide evidence on its first turn. If it
  also fails, notify the user and take over transparently.
- If a required role is unavailable, report it; do not silently take over the
  complete specialized workflow.
- Wait about 60 seconds during active work. Avoid polling or filesystem checks
  merely to detect worker activity.
- Update the user only at meaningful transitions: assignment, handoff, verified
  defect, replacement/takeover, blocker, or completion.
- Record material blockers with the failed step, evidence, suspected cause,
  completed state, affected criterion, and required next action.
- Never present partial work as complete.

## Usage and Session End

At the end of each shift and in the final report, use a compact table with call
counts for `executor_luna`, `executor_sol`, `tester`, and `doc-writer`; add
companion usage from `~/.codex/codex_workflow/explorer_companion.md`.

When the user says the exact phrase `end this session`, ignoring capitalization
and surrounding punctuation, follow
`~/.codex/codex_workflow/end_of_session.md` under the Heavy branch.
