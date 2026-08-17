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

Workers never own Git or external delivery by default. There is no persistent
explorer, automatic session closer, automatic documentation sweep, or automatic
commit.

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
- Medium delegates one bounded package to the best matching role.
- Heavy uses multiple workers only for independent ownership or independent
  implementation and acceptance.

The coordinator chooses the smallest sufficient route unless the user requests
one explicitly. Every initial worker receives a compact capsule with
`fork_turns="none"`; repository history is referenced rather than copied.
