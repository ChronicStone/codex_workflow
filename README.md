# Codex Workflow

A general-purpose Codex orchestration setup that keeps a GPT-5.6 Sol coordinator
focused on architecture and integration while GPT-5.6 Luna workers handle
bounded execution, investigation, testing, and review.

The workflow is tuned for full-stack applications, frontend product work,
libraries, automation, and mixed repositories. Its delegation policy is loaded
globally, while project `AGENTS.md` files and skills remain authoritative for
repository-specific work.

## Default model pair

Add the coordinator model to `~/.codex/config.toml`:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
```

The installer owns these native subagent settings:

```toml
[agents]
enabled = true
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "xhigh"
max_concurrent_threads_per_session = 4
max_depth = 1
```

Four workers is a deliberate default: it permits useful parallelism without
encouraging duplicated repository reads or overlapping edits. Configuration
supports up to eight when the workload consistently decomposes cleanly.

## Roles

| Role | Model | Purpose |
| --- | --- | --- |
| `scout` | Luna xhigh | Read-only repository, architecture, dependency, and root-cause investigation |
| `implementer` | Luna xhigh | General backend, full-stack, library, automation, and configuration work |
| `ui-implementer` | Luna xhigh | Visible frontend implementation with browser verification |
| `tester` | Luna xhigh | Independent behavioral verification and regression coverage |
| `reviewer` | Luna xhigh | Independent correctness, ownership, security, and regression review |
| `ui-reviewer` | Luna xhigh | Rendered visual, interaction, responsive, and accessibility acceptance |
| `doc-writer` | Luna xhigh | Targeted durable documentation |

Luna stays at `xhigh` because reducing expensive Sol work is the optimization
target; worker count, reuse, ownership, and evidence consumption control waste.

Use `<role> — <task ID>` for agent references in commentary, plans, worker
ledgers, and final reports, keyed by native `agent_id`. Generated person
nicknames may appear only inside a quoted native platform error; no nickname or
display-name configuration is supported, and every worker capsule includes its
task ID.

Workers never own Git or external delivery by default. There is no persistent
Explorer, automatic session closure, automatic documentation sweep, or automatic
commit. The default task budget is six cumulative workers, separate from the
four-worker concurrency cap.

## Installation

Download a release asset and verify it against `SHA256SUMS`, then ask Codex to
read the bundled `codex_workflow/bootstrap.md` and follow it. Python 3.11 or
newer is required.

After bootstrap, restart Codex. Every repository inherits the workflow; this
command only verifies the global installation:

```text
codex_workflow --install
```

Configuration and lifecycle commands are documented in
[`workflow_usage.md`](workflow_usage.md).

## Routing

- Light works directly for questions, diagnosis, plans, and small changes.
- Medium delegates exactly one initial worker, with follow-ups reusing it and no
  replacement worker.
- Heavy allocates 2-4 independent initial workers and never exceeds six total;
  repairs return to the responsible implementer, and independent review runs
  only when the user asks or a concrete risk requires it.

Delegation is opt-in. Only `workflow medium`, `workflow high`/`workflow heavy`,
or a direct request to delegate, spawn, or use subagents activates it. Model or
reasoning selections such as `Luna high` never select a route; without an
explicit trigger the task stays Light, regardless of size. Every initial worker
receives a compact capsule with `fork_turns="none"`; repository history
is referenced rather than copied. Waiting is event-driven: use one long native
wait or background monitor rather than coordinator polling or repeated status
turns. Valid worker evidence is consumed unless conflict, staleness, an
integration boundary, or high risk reopens it.

Validation follows a deduplicated ladder: the implementing Luna worker runs the
smallest focused check when a coherent slice should pass and one owner gate at
handoff; a tester covers only an otherwise-unchecked risk; Sol runs only a
missing integration or explicitly required shipping gate. Passing evidence is
reused until its scoped inputs change, and a readiness command that subsumes
owner checks runs once rather than back-to-back with them.
