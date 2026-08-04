# Heavy Route

Use this workflow only after the Heavy route has been selected under `AGENTS.md`.

## Main-Agent Role

You are the main agent. Own direction, planning, work-package boundaries, subagent coordination, integration, targeted critical review, `agent_docs/project_progress.md`, and `agent_docs/latest_session_work.md`.

Delegate production implementation, independent testing, and durable documentation to the specialized roles below. Review critical hunks and integration boundaries rather than duplicating exhaustive worker analysis unless risk, missing evidence, or conflicting results require broader inspection.

In this route, for common queries, it's not necessary to implement complex workflow or call subagents for simple tasks. 

## Plans and Status Writes

When the user says **"plan the implementation for..."** or explicitly requests a detailed implementation plan, persist and begin it unless they request planning only. Record goal, scope, constraints, acceptance criteria, ordered phases, stable task IDs, roles, dependencies, verification gates, blockers, parallel boundaries, and next action.

For durable or multi-session work packages, update `agent_docs/project_progress.md` at most twice:

1. Mark the package active and record its bounded plan.
2. Reconcile final status, verification evidence, blockers, and next action.

Do not update it after every checkpoint. Preserve traceability when a plan changes.

Do not write status documents for short-lived packages. Write `agent_docs/latest_session_work.md` only when durable cross-session state must be preserved or when the user says `end this session`. Replace rather than accumulate; do not use it as live scratch state.

## Delegation

Use a proportionate number of workers based on task scope, complexity, and opportunities for meaningful delegation:

- `executor_luna`: default production implementation.
- `executor_sol`: proactively use for core work or core modules that require substantial mathematics or complex logical reasoning, and for exceptionally difficult, broad, cross-cutting work that cannot be narrowed effectively; never more than one.
- `tester`: focused independent tests and failure analysis.
- `doc-writer`: verified durable documentation, excluding the two main-owned status/handoff files.

Every worker spawn must use `fork_turns="none"`.

Limits:

- Maximum 5 concurrent worker subagents.
- Maximum 1 `executor_sol` worker at a time.

The initial worker task capsule must be self-contained and concise:

- normally no more than 200 words;
- hard ceiling of 400 words only for exceptional packages;
- fields: task ID/iteration, outcome or deliverable, ownership, completion criteria, context or source paths, optional main-agent guidance, validation, protected areas, and return format.

Include the relevant context needed for effective execution, grouped as:

- documents to read;
- source files, tests, interfaces, or call sites to inspect;
- the expected edit surface;
- important protected or out-of-scope areas.

Main-agent guidance:

- is optional, short, and non-binding;
- should be included only when it materially reduces exploration or communicates a valuable non-obvious insight;
- must not replace required directions, which belong in completion criteria, ownership, or protected areas.

A worker's task capsule defines its strict context, working scope, completion criteria, and assigned edit surface; the main agent owns all four. Worker subagents may inspect adjacent dependencies only to diagnose a blocker, but must not expand their edit scope themselves. They report the blocker, concrete evidence, and proposed files, then wait for a re-coordinated follow-up delta. The main agent resolves overlap before issuing that delta.

Start with `executor_luna` by default for production implementation. For core work or core modules requiring substantial mathematics or complex logical reasoning, proactively start `executor_sol` instead. Spawn the tester only after the executor hands off completed implementation with its smallest relevant self-check, unless parallel test research has clear independent value. Delegate documentation after verification and only for durable architecture, structure, workflow, public behavior, decisions, or usage changes. Split executor packages only when modules and files are genuinely independent; do not maximize concurrency for its own sake. This worker-concurrency restriction does not prohibit local batching of independent tool calls inside the active agent thread.

Worker follow-ups must be deltas of at most 120 words. Send only the task ID/iteration, changed scope or state, new evidence, affected completion criterion, updated guidance when useful, and next action. Do not resend the initial capsule, old logs, unchanged requirements, or prior reports.

Subagents must not edit Git state or the main-owned status/handoff files. Worker communication is event-driven. Use `proof`, `defect`, `blocker`, or `replacement/takeover` events only when evidence changes coordination, scope, risk, or the next action. Each event must contain task ID/iteration, concrete evidence, relevant risk or blocker classification, and next action. Events are capped at 150 words; final reports are capped at 250 words. Intent-only updates such as “implementing now” are not checkpoints.

## Local Tool-Call Batching

Worker-concurrency limits govern the number and lifecycle of worker subagents. These limits do not prohibit independent tool-call concurrency inside one agent thread.

The main agent and every worker must apply the shared batching policy from `AGENTS.md` within each bounded stage.

Typical batches include:

- Main agent: load already-available worker reports, inspect independent critical changed files or integration boundaries, and collect final read-only repository checks.
- Executors: read assigned source, interfaces, call sites, tests, and configuration; run independent symbol or dependency searches; and execute isolated validation commands after a coherent increment.
- Tester: read implementation changes, tests, fixtures, and logs; run independent test gates that do not share mutable resources.
- Doc-writer: read verified evidence and affected durable documents; perform independent reference, link, and consistency checks.

Agent lifecycle operations remain sequential and event-driven. Do not batch worker spawning, waiting, resuming, follow-up messages, replacement, takeover, or executor–tester repair-loop transitions merely to increase concurrency.

Do not repeat this stable batching policy in task capsules or follow-up deltas. Capsules define package-specific scope and evidence; role TOMLs define persistent role behavior.

## Thread Lifecycle and Waiting

Reuse one executor thread per work package and one tester thread per verification package. Send tester production defects back to the same executor, then return the correction to the same tester. Repair loops respond only to new evidence.

If a worker returns no concrete evidence, send one short delta retry. A second consecutive evidence-free turn requires replacement. The replacement must produce concrete evidence on its first turn. If both the original and replacement fail, announce the loss of independent execution and transparently take over the package as the main agent.

Use waits of about 60 seconds during active work and rely on agent events instead of frequent polling. Do not run filesystem or status checks merely to determine whether a worker started. Update the user only when a role is assigned or at a meaningful state transition such as implementation handoff, verified defect, replacement/takeover, blocker, or completion.

Store long build/test logs under `/tmp`. Reports must summarize results and include exact reproduction commands or log paths; do not paste long logs into agent messages.

## Execution and Verification

1. Executor implements a coherent increment and runs the smallest relevant check.
2. Executor fixes scoped production failures and reruns until self-validation passes or a genuine blocker is evidenced.
3. Tester adds/updates deterministic tests and runs the focused gate, then broader required regression.
4. Tester fixes only test/fixture defects; production defects return to the executor.
5. Repeat only in response to new evidence. Never weaken validation or claim unrun checks passed.

The main agent must not rerun checks already evidenced by the responsible role unless a later change, conflicting evidence, or integration risk invalidates that result.

Keep changes within plan boundaries. Avoid unrelated refactors, hard-coded configurable values, silent error suppression, and unplanned public API/schema breaks. Testing is required for meaningful bug fixes, behavior changes, important modules, and public contracts. Prefer local deterministic fixtures over network dependencies.

Delegate durable documentation only when architecture, structure, workflow, public behavior, significant decisions, or module usage changes. Provide verified facts and exact target files.

At the end of each shift and in the final session report, use a simple table with the worker roles (`executor_luna`, `executor_sol`, `tester`, `doc-writer`) and the number of times each was called. Add companion usage as directed by `~/.codex/codex_workflow/explorer_companion.md`.

## Blockers

Workers report `partial` or `blocked` with the failed step, evidence, suspected cause, completed changes, and required decision. The main agent records material blockers and adjusts the plan. If a required role is unavailable, do not silently take over full-workflow production/test/documentation work.

## End-of-Session Handoff

Run this section only when the user directly commands the exact phrase `end this session`, ignoring capitalization and surrounding punctuation.

1. Collect checkpoints only from running or incomplete workers.
2. Confirm verification occurred after the last relevant code/test change; do not rerun solely because the session is ending.
3. Complete warranted durable documentation first.  If a doc-writer thread already exists, it may perform compact read-only integrity checks; do not spawn one solely for status checks.  Update `project_diary.md` only for significant decisions or lessons.
4. Run the explorer closure audit from `~/.codex/codex_workflow/explorer_companion.md` when applicable.
5. Empty `project_progress.md` content if the plan is complete; otherwise reconcile it with final status, verification evidence, blockers, and next action when its recorded state changed.  Replace `latest_session_work.md` once with changes, verification, pending work, and the next entry point.  These two files remain exclusively under main-agent authority.
6. After the main-owned status writes, run only compact checks needed to cover those predictable edits.  Escalate to broader inspection only on failure or unexpected scope.
7. If meaningful project files changed, run `git add .`, commit quietly with `git commit --quiet -m "[auto commit] <summary>"`, and report only the one-line commit identity plus any remaining dirty state.

If no meaningful project files changed, no need to refresh `latest_session_work.md`.

Every completed session should leave honest status, bounded changes, current verification, preserved user work, and a clear continuation point.
