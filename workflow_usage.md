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

Each initialized project receives a managed delegation section in `AGENTS.md`,
a protected project-local instruction region, and hidden lifecycle state.
Existing project instructions are preserved in the
project-local region and remain authoritative for domain work.

## Commands

| Prompt | Effect |
| --- | --- |
| `codex_workflow --install` | Initialize the current project using the installed user runtime |
| `codex_workflow --configure` | Change Luna effort, concurrency, or report size |
| `codex_workflow --personal` | Configure project-specific workflow preferences |
| `codex_workflow --check-update` | Check releases without mutation |
| `codex_workflow --update` | Verify and install the latest eligible release |
| `codex_workflow --disable` / `--enable` | Disable or restore the project entry point |
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
  "schema_version": 5,
  "default_executor": "implementer",
  "default_executor_reasoning_effort": "xhigh",
  "default_subagent_model": "gpt-5.6-luna",
  "default_subagent_reasoning_effort": "xhigh",
  "auto_check_update": false,
  "max_concurrent_workers": 4,
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

The lifecycle CLI patches only workflow-owned `[agents]` keys and owned role
files. It preserves unrelated `config.toml`, user instructions, workers, and
project content. Removal deletes the workflow runtime and owned roles while
preserving project documentation and unrelated Codex state.

## Delegation contract

The coordinator selects roles from task shape:

- use `scout` when bounded discovery would otherwise pollute Sol context;
- use `implementer` for general production code;
- use `ui-implementer` for visible changes requiring browser evidence;
- use `tester` when independent behavioral verification materially lowers risk;
- use `reviewer` for an independent diff or branch review;
- use `ui-reviewer` for actual rendered acceptance after visible changes;
- use `doc-writer` only for assigned durable documentation.

Every initial worker receives `fork_turns="none"` plus the outcome, owner,
surface, protected areas, relevant decisions and references, recommended
approach, invariant, likely pitfall, acceptance criteria, validation, and
escalation conditions. Workers return evidence and knowledge deltas rather than
logs or repeated repository context.

## Safety and lifecycle

The workflow never automatically commits, pushes, publishes, deploys, migrates
shared systems, or performs an end-of-session documentation sweep. Those
actions require explicit user intent and remain coordinator-owned. Parallel
workers must not share mutable build output, fixtures, databases, ports,
browsers, devices, or overlapping edit surfaces.
