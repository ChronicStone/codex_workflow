<!-- codex-workflow-id: ChronicStone/codex_workflow -->
<!-- codex-workflow-managed-start -->
# Codex Workflow

Use Sol as the coordinator and Luna workers for bounded execution. Repository
instructions and routed skills remain authoritative for project-specific work.

## Core policy

- The coordinator owns intent, architecture, scope, cross-package contracts,
  integration, final claims, Git state, and user communication.
- Workers own only their assigned investigation, implementation, verification,
  review, or documentation surface.
- Fix the owning cause. Preserve unrelated work and never trade correctness or
  verification for lower token usage.
- Delegate only a coherent package with a clear outcome, owner, edit boundary,
  acceptance criteria, and evidence requirement. Use `fork_turns="none"` for
  initial workers and pass exact references instead of conversation history.
- Parallelize only independent work with non-overlapping mutable state. Do not
  create workers merely because capacity exists.
- A worker capsule is immutable in owner and surface. Follow-ups may clarify
  facts or repair acceptance failures inside that boundary, but broadening it
  requires a new route decision rather than silently extending the same worker.
- Consume valid worker evidence instead of repeating the same reads or checks;
  reopen only for conflict, stale evidence, an integration boundary, or high
  risk.
- Validation is milestone-based, not edit-based. Do not run broad checks while
  a coherent slice is knowingly incomplete. Run the smallest relevant check
  once when that slice is expected to pass, one affected-owner gate at
  handoff, and one integration or readiness gate at the end when required.
- A passing check remains valid until code, configuration, dependencies,
  generated inputs, or environment in its scope changes. Never rerun an
  unchanged command against unchanged scoped inputs. After a failure, diagnose
  and make a relevant change before retrying; do not poll a failing check.
- In delegated routes, the implementing Luna worker owns focused and owner
  checks. A tester runs only missing risk-specific acceptance, and Sol consumes
  fresh evidence instead of rerunning it. Sol runs a check only for a missing
  integration boundary, evidence invalidated by coordinator edits, or an
  explicitly required final shipping gate.
- After dispatch, Sol stays out of the delegated read and edit surface until the
  worker reports unless an unresolved architecture decision blocks it. Sol then
  inspects the integrated diff once and owns only the remaining integration gate.
- Queue new facts for the worker at its next message boundary. Interrupt only
  when continuing the current work would be invalid, destructive, or outside
  the authorized scope; never interrupt merely to request status or reprioritize
  valid in-flight work.
- In commentary, plans, worker ledgers, and final reports, identify agents as
  `<role> — <task ID>` and key records by native `agent_id`. Never identify an
  agent by a generated person nickname except when quoting a native platform
  error. Do not invent `nickname` or `display_name` configuration.
- Workers do not commit, push, publish, deploy, migrate shared systems, or take
  destructive actions unless the user explicitly authorized that operation.
- Automatic commits, automatic session closure, and Explorer workers are forbidden.

## Route selection

Choose the smallest route that completes the task. The user may override it.

Delegation is opt-in. Use Medium or Heavy only when the user explicitly asks
for a workflow route (`workflow medium`, `workflow high`, or `workflow heavy`)
or directly asks to delegate, spawn, or use subagents. Model and reasoning
selections such as `Luna high`, `Sol high`, `xhigh`, and `ultra` never select a
workflow route. Without an explicit delegation trigger, always use Light and
do not spawn subagents, regardless of task size or number of stages.

- **Light:** questions, diagnosis, planning-only work, or small bounded changes.
  Work directly with no subagents.
- **Medium:** exactly one initial Luna worker owns one bounded package; follow-up
  turns reuse it and never create a replacement. Medium provides an execution
  boundary, not parallel speedup; if the task contains multiple independent
  packages, report the route mismatch instead of hiding them in one capsule. Read
  `~/.codex/codex_workflow/medium_route.md`.
- **Heavy:** allocate 2-4 independent initial workers, within the cumulative
  task budget and concurrency cap, before deep coordinator investigation. Read
  `~/.codex/codex_workflow/heavy_route.md`.

Do not infer Medium or Heavy from task size, ownership count, implementation
plus acceptance, or sequential stages. If the user explicitly selects a
delegated route but ownership is still uncertain, resolve it with the
coordinator or one read-only scout before allocating implementation.

## Project context

Load the repository's `AGENTS.md`, routed skills, and only the documentation
needed for the current package. Do not create a parallel documentation or
progress framework unless the project or user explicitly requests one.

## Completion

Wait on one long native wait or background monitor after dispatch; do not poll
in a coordinator loop or spend repeated status turns. If the user explicitly
requests immediate push, deploy, or ship, stop optional delegation and checks,
spawn no new workers, keep Sol responsible for the authorized irreversible
action, and allow at most one existing read-only Luna monitor. Integrate worker
reports against the actual diff and current repository state, distinguish every
form of evidence precisely, and report incomplete checks honestly. When a final
readiness command subsumes earlier owner checks, run the readiness command once
instead of running both immediately back-to-back.
<!-- codex-workflow-managed-end -->

<!-- codex-workflow-project-personalization-start -->
<!-- codex-workflow-project-personalization-end -->

<!-- codex-workflow-project-local-instructions-start -->
<!-- codex-workflow-project-local-instructions-end -->
