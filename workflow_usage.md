# Workflow Usage

## Installed layout

```text
~/.codex/
├── AGENTS.md
├── config.toml
├── agents/
│   ├── scout.toml
│   ├── implementer.toml
│   ├── ui-implementer.toml
│   ├── tester.toml
│   ├── reviewer.toml
│   ├── ui-reviewer.toml
│   └── doc-writer.toml
└── codex_workflow/
    ├── workflow.py
    ├── workflow_config.json
    ├── light and heavy route guidance
    ├── lifecycle runtime
    └── templates and backups
```

The managed delegation policy lives in global `~/.codex/AGENTS.md`, so every
repository inherits it without project installation. Repository `AGENTS.md`
files remain untouched and provide the more specific domain rules.

## Commands

| Prompt | Effect |
| --- | --- |
| `codex_workflow --install` | Verify that the global workflow is installed |
| `codex_workflow --configure` | Change Luna effort, concurrency, or report size |
| `codex_workflow --check-update` | Check releases without mutation |
| `codex_workflow --update` | Verify and install the latest eligible release |
| `codex_workflow --remove` | Show a destructive dry run, then remove owned workflow files after confirmation |

Automatic update checks are disabled by default. Enable or disable the
notification-only session check with
`codex_workflow --enable_auto_check_update` and
`codex_workflow --disable_auto_check_update`.

## Configuration

The mutable source is
`~/.codex/codex_workflow/workflow_config.json`. Generated TOML and route files
must not be edited directly.

```json
{
  "schema_version": 6,
  "default_executor": "implementer",
  "default_executor_reasoning_effort": "xhigh",
  "default_subagent_model": "gpt-5.6-luna",
  "default_subagent_reasoning_effort": "xhigh",
  "auto_check_update": false,
  "max_concurrent_workers": 4,
  "max_total_workers": 6,
  "report_package_size": 200,
  "enabled_workers": [
    "scout",
    "implementer",
    "ui-implementer",
    "tester",
    "reviewer",
    "ui-reviewer",
    "doc-writer"
  ]
}
```

The lifecycle CLI patches only its marked global instruction region,
workflow-owned `[agents]` keys, and owned role files. It preserves unrelated
`config.toml`, user instructions, workers, and every repository file. Removal
deletes the global workflow runtime and owned roles while preserving unrelated
Codex and project state.

## Delegation contract

Delegation is opt-in. A user must explicitly request `workflow medium`,
`workflow high`/`workflow heavy`, delegation, spawned agents, or subagents.
Selecting a model or reasoning level such as `Luna high` never activates a
route; absent an explicit trigger, the coordinator works directly with no
subagents.

The coordinator selects roles from task shape:

- use `scout` when bounded discovery would otherwise pollute Sol context;
- use `implementer` for general production code;
- use `ui-implementer` for visible changes requiring browser evidence;
- use `tester` when independent behavioral verification materially lowers risk;
- use `reviewer` for an independent diff or branch review;
- use `ui-reviewer` for actual rendered acceptance after visible changes;
- use `doc-writer` only for assigned durable documentation.

Medium creates exactly one initial worker and reuses it for follow-ups without a
replacement. Heavy creates 2-4 independent initial workers within the six-worker
cumulative task budget and reuses the responsible implementer for repairs.
Independent review runs only when the user asks or a concrete risk requires it.
Do not repeat scouts or reviewers over the same surface.

Identify agents as `<role> — <task ID>` in commentary, plans, worker ledgers, and
final reports, keyed by native `agent_id`. Generated person nicknames are never
used except when quoting a native platform error. Every capsule includes the
task ID, and the workflow adds no `nickname` or `display_name` setting.

Every initial worker receives `fork_turns="none"` plus the outcome, owner,
surface, protected areas, relevant decisions and references, recommended
approach, invariant, likely pitfall, acceptance criteria, validation, and
escalation conditions. Workers return evidence and knowledge deltas rather than
logs or repeated repository context.

## Validation cadence

Checks have one owner and run at milestones rather than after every edit. The
implementing Luna worker runs the smallest focused check once when its slice is
expected to work, then one affected-owner gate before handoff. A tester runs
only missing risk-specific acceptance, and Sol consumes fresh evidence instead
of repeating it. A passing result remains valid until scoped code,
configuration, dependencies, generated inputs, or environment changes. Retry a
failure only after diagnosis and a relevant change. Run a final integration or
readiness gate once when required; if it subsumes owner checks, do not run both
back-to-back.

## Safety and lifecycle

The workflow never automatically commits, pushes, publishes, deploys, migrates
shared systems, or performs an end-of-session documentation sweep. Those
actions require explicit user intent and remain coordinator-owned. Parallel
workers must not share mutable build output, fixtures, databases, ports,
browsers, devices, or overlapping edit surfaces.

Use one long native wait or background monitor for delegated work; do not poll in
a coordinator loop or repeat status model turns. If the user explicitly asks to
push, deploy, or ship immediately, stop optional delegation and checks, spawn no
new workers, keep Sol responsible for the authorized irreversible action, and
allow at most one existing read-only Luna monitor.
