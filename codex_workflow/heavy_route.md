# Heavy Route

Use after the Heavy route is selected under `AGENTS.md`.

<!-- codex-workflow-effective-config-start -->
## Effective Workflow Configuration

- Default executor: `executor_luna` (`xhigh` reasoning effort).
- Enabled workers: `executor_luna`, `executor_sol`, `tester`, `doc-writer`, `explorer`, `end_of_session`.
- Maximum concurrent child workers: `20`.
- Maximum `executor_sol` workers: `1`.
- Maximum worker final-report package: `250` words.
- End-of-Session context fork: `200` recent turns.

Create only enabled workers and obey these limits.
<!-- codex-workflow-effective-config-end -->

## Main-Agent Role

You are the main agent.
Minimize main-agent token use while preserving decision quality, clear ownership,
and reliable verification.

The main agent owns:

- Direction, scope, acceptance criteria, plan, and task IDs.
- Package boundaries, dependencies, ownership, and strategic coordination.
- Critical review, integration decisions, verification gates, and completion.
- Git state, user communication, and official status during normal execution.
  The dedicated handoff worker takes ownership of Git state and the two status
  documents only during End-of-Session.

Read foundational context, critical interfaces, and decision-driving evidence.
Delegate supporting context to Explorer and package-local discovery,
implementation, self-check, and repair to workers. Broaden main-agent review
only for high risk, missing evidence, or conflicting results. Worker TOMLs own
internal implementation, testing, batching, and reporting behavior. Do not
repeat those instructions here or in task capsules.

Simple queries do not require delegation.

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

Do not write status for short-lived work or after every checkpoint. Put detailed
current work, verification, blockers, and the exact continuation point in
`agent_docs/latest_session_work.md` only for a durable cross-session handoff;
replace its content and never use it as scratch space. The main agent owns both
files during normal execution. The `end_of_session` worker owns them during an
invoked handoff; all other workers may only provide compact verified inputs.

## Delegation

Delegate coherent, independently completable packages. Each package should be
large enough for one worker to handle its local discovery, implementation,
self-check, and focused repair. Run packages concurrently when their outcomes
and ownership of mutable resources are independent. Do not fragment work merely
to increase worker count or concurrency.

- Selected default executor (`executor_luna` or `executor_terra`): production implementation.
- `executor_sol`: when enabled, reserve for core work requiring substantial
  mathematical or logical reasoning, or exceptionally difficult cross-cutting
  work that cannot be narrowed effectively.
- `tester`: independent verification; normally starts after executor self-check,
  unless parallel test research has clear independent value.
- `doc-writer`: after verification, for durable architecture, structure,
  workflow, public behavior, decisions, or usage; never the two status files.
- `explorer`: follow `~/.codex/codex_workflow/explorer_companion.md`; it is a
  companion rather than a task worker, but its live thread consumes platform
  child-agent capacity.
- `end_of_session`: fresh handoff owner for Medium and Heavy routes; follow
  `~/.codex/codex_workflow/end_of_session.md`.

Every initial task-worker capsule must use `fork_turns="none"`, normally stay
within 200 words, and never exceed 400 words. The dedicated End-of-Session
worker instead uses the configured finite recent-turn fork and receives no
capsule beyond the route and extra user handoff details. Task-worker capsules
include only:

- Task ID/iteration and bounded outcome.
- Ownership and expected edit surface.
- Relevant documents, source, interfaces, call sites, dependencies, and upstream
  decisions.
- Acceptance criteria and validation.
- Protected areas and return format.

For the default executor, include main-agent guidance: a recommended approach,
its rationale, and the most important invariant, integration risk, or likely
pitfall. For `executor_sol`, provide decision context and constraints but no
proposed solution; let it derive the approach independently.

If work must expand, require evidence and proposed files, resolve overlap, then
send a scoped follow-up. Follow-ups stay within 120 words and contain only task
ID/iteration, changed scope or state, new evidence, affected criterion, useful
updated advice, and next action. Do not resend unchanged context or old logs.

Expect one concise, evidence-backed completion report per package. Workers
contact the main agent earlier only for scope expansion, ownership conflicts, or
decision-blocking ambiguity. Obey configured worker limits. Keep cross-package
lifecycle gates sequential and evidence-driven. Keep one child-agent slot
available for the required End-of-Session worker.

## Handoff and Verification

1. Executor returns a coherent implementation and focused self-check evidence.
2. Main agent reviews scope, critical changes, and integration boundaries.
3. Tester runs focused and required regression verification.
4. Test/fixture defects stay with tester; production defects return to the same
   executor, then to the same tester.
5. Delegate durable documentation only after relevant behavior is verified.
6. Main agent reconciles final evidence during normal execution; an invoked
   End-of-Session delegates final status and Git handoff to its dedicated worker.

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
- Wait for worker lifecycle events. Do not poll workers, inspect the filesystem
  merely to detect activity, or request routine progress reports.
- Update the user only at meaningful transitions: assignment, handoff, verified
  defect, replacement/takeover, blocker, or completion.
- Record material blockers with the failed step, evidence, suspected cause,
  completed state, affected criterion, and required next action.
- Never present partial work as complete.

## Usage and Session End

At the end of each shift and in the final report, use a compact table with call
counts for the selected default executor (`executor_luna` or `executor_terra`),
`executor_sol`, `tester`, `doc-writer`, and `end_of_session`; add
companion usage from `~/.codex/codex_workflow/explorer_companion.md`.

When the user says the exact phrase `end this session`, ignoring capitalization
and surrounding punctuation, follow the delegation contract in
`~/.codex/codex_workflow/end_of_session.md`.
