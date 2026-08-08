# codex_workflow — Workflow Usage Guide

`codex_workflow` is a modular Codex workflow with explicit responsibility
boundaries, persistent project documentation, shared user-level runtime files,
and conservative lifecycle operations.

This guide is organized into five parts:

1. command prompts and route selection;
2. the installed-file map;
3. manual configuration and customization;
4. the Heavy-route execution model;
5. the component hierarchy and ownership model.

## Part 1 — Command prompts and everyday use

### First-time bootstrap

Open Codex from the project directory and send this prompt:

```text
Download the prerelease GitHub Release tagged `v1.1.0` from https://github.com/viettran-edgeAI/codex_workflow/releases. Download the universal asset `codex_workflow-1.1.0.zip` and `SHA256SUMS`, verify the ZIP checksum, and extract the ZIP to a temporary directory. Do not clone the repository, download a source-code archive, or use `README.md` as an installation source. Then read the extracted `codex_workflow/install.md` and follow it exactly to complete the first installation for this project.
```

The release package is a universal ZIP for Linux, macOS, and Windows. The
installation guide inside the package is the source of truth for validation,
copying, backups, project initialization, and completion checks. After the
first installation, start a new Codex session so the newly installed user
instructions are loaded.

The bootstrap installs the user-level workflow and the current project. It
does not ask configuration or personalization questions. Those are explicit
follow-up commands.

### Exact command prompts

Send each command as its own prompt. These are workflow instructions handled by
Codex, not operating-system executables.

#### `codex_workflow --configure`

Interactively change the persistent user-level workflow configuration:

- default executor (`executor_luna` or `executor_terra`);
- default executor reasoning effort (`high`, `xhigh`, or `max`);
- maximum concurrent workers;
- maximum concurrent `executor_sol` workers;
- final-report package size.

The command shows the current values, proposes a complete new JSON snapshot,
and writes only after confirmation. It then synchronizes the Heavy route,
active workflow worker TOMLs, and workflow-owned Codex platform settings. It
does not change project personalization or project documents.

#### `codex_workflow --personal`

Interactively personalize the current project. The three supported areas are:

1. Frontend Project Profile, including a project-specific verification profile
   such as reduced frontend testing when that is an intentional decision;
2. Design Principles;
3. Additional Workflow Decisions.

Confirmed decisions are stored in the hidden project resource and materialized
inside the personalization marker in the project's workflow entry point. A
missing or invalid resource is only staged as a recovery proposal until
confirmation; cancellation changes no file. This command does not modify global
worker configuration or the Project Documentation Framework.

#### `codex_workflow --install`

Install or enable the workflow in the current project after the user-level
workflow has already been bootstrapped. It recognizes the active
`AGENTS.md` or the disabled hidden entry point and:

- creates or preserves the project `AGENTS.md` entry point;
- creates missing files in `agent_docs/` from the six project-document
  templates;
- initializes only newly created documentation with `doc-writer`;
- creates the default hidden personalization resource when missing;
- reuses the installed user-level configuration.

It does not reinstall the user-level payload, reset existing project documents,
or ask configuration and personalization questions.

#### `codex_workflow --update`

Update the installed workflow and the recognized current project from a GitHub
Release asset. The command queries the GitHub Releases API, selects the latest
eligible semantic-versioned release with the matching ZIP and checksum,
downloads the asset, verifies it, and extracts it into a temporary directory.
It never clones or pulls the repository.

The update preserves valid configuration, project personalization, project
documents, unrelated workers and settings, source backups, and the project's
enabled or disabled state. It preflights the recognized project and resolves
conflicts before replacing any live user-level files, then applies a staged
update with rollback on write failure.

Use `codex_workflow --update --source <PACKAGE>` to update or repair from one
local extracted release package instead. This form skips GitHub release lookup
and uses the supplied package path directly.

#### `codex_workflow --check-update`

Perform a read-only version check. Codex reads the installed `VERSION`, queries
GitHub Releases, filters out unusable release records and mismatched assets,
compares semantic versions, and reports whether an appropriate newer release
is available.

This command does not download, extract, modify, clone, or pull anything. It
requires network access for automatic lookup but does not require Git.

#### `codex_workflow --disable`

Disable the workflow for the current project by moving the active entry point:

```text
AGENTS.md -> .codex_workflow_hidden_resource/.AGENTS.md
```

The contents, personalization resource, project documents, and user-level
workflow remain intact. The operation is a safe no-op when the project is
already disabled.

#### `codex_workflow --enable`

Re-enable a disabled project by moving the entry point back:

```text
.codex_workflow_hidden_resource/.AGENTS.md -> AGENTS.md
```

This changes only the active/disabled entry-point state. It does not reread or
reapply configuration or personalization.

### Route selection and session closure

There are three execution routes:

- **Light route** — the default; the main agent works alone with minimal
  workflow overhead.
- **Medium route** — full planning and documentation discipline without worker
  subagents.
- **Heavy route** — the main agent orchestrates enabled worker subagents for
  larger deployment-state tasks.

For ordinary questions and small tasks, no route command is needed. To select
a route for a task or plan, include one of these instructions in the prompt:

```text
use medium route. [task description]
use heavy route. [task description]
```

The selected route remains active until the user changes it or ends the
session. To perform the handoff and update durable project state, send:

```text
end this session
```

The shared End-of-Session procedure verifies the final state and updates the
cross-session documentation when warranted.

## Part 2 — Installed-file map

The release ZIP contains only one top-level directory, `codex_workflow/`. It
does not contain the repository README, README images, development documents,
`.git/`, release scripts, or other repository-only files. On Windows, `~/.codex`
means the current user's profile directory and the platform's normal path
separator is used.

After installation, the runtime is distributed between the user environment
and the current project as follows:

```text
~/.codex/
├── AGENTS.md                              # user-level command interface
├── config.toml                            # existing Codex config; only workflow-owned keys are managed
├── agents/                                # active workflow worker TOMLs
│   ├── executor_luna.toml
│   ├── executor_sol.toml
│   ├── tester.toml
│   ├── doc-writer.toml
│   └── explorer.toml
└── codex_workflow/
    ├── VERSION                             # installed workflow version
    ├── user_AGENTS.md                      # managed command marker and command prompts
    ├── workflow_config.json                # persistent workflow configuration
    ├── heavy_route.md                      # Heavy-route orchestration rules
    ├── medium_route.md                     # Medium-route rules
    ├── explorer_companion.md               # read-only Explorer lifecycle and boundaries
    ├── end_of_session.md                   # shared session handoff procedure
    ├── install.md                          # installation procedure
    ├── update.md                           # Release-based update procedure
    ├── check_update.md                     # read-only Release-based version check
    ├── configuration_guide.md               # --configure procedure
    ├── personalization_guide.md            # --personal procedure
    ├── disable.md                          # --disable procedure
    ├── enable.md                            # --enable procedure
    ├── templates/
    │   ├── AGENTS.md                       # project entry-point template
    │   ├── agents/*.toml                    # all distributed worker templates
    │   └── project_docs/*.md                # six Project Documentation templates
    ├── .source_backup/<version>/            # complete installed release source backup
    └── .backups/<old-version>-<timestamp>/ # update backups, created when needed

<project>/
├── AGENTS.md                               # active project workflow entry point
├── agent_docs/
│   ├── project_overview.md
│   ├── project_core_tech.md
│   ├── project_structure.md
│   ├── project_progress.md
│   ├── project_diary.md
│   └── latest_session_work.md
└── .codex_workflow_hidden_resource/
    ├── personalization.md                  # project-scoped private resource
    └── .AGENTS.md                          # disabled entry point; mutually exclusive with root AGENTS.md
```

The last two project entry-point files are mutually exclusive: an enabled
project has `AGENTS.md`; a disabled project has the hidden `.AGENTS.md`. The
hidden directory is also where project personalization is kept so it is not
mistaken for ordinary project documentation.

The six files under `agent_docs/` have different ownership and purposes:

- `project_overview.md` — goals, architecture, workflow, and major decisions;
- `project_core_tech.md` — important technologies and architectural constraints;
- `project_structure.md` — layout, modules, ownership, and boundaries;
- `project_progress.md` — active deployment plan and cross-session status;
- `project_diary.md` — durable decisions, discarded approaches, and lessons;
- `latest_session_work.md` — the latest handoff and unfinished work.

## Part 3 — Manual configuration and customization

The command prompts are the safe default because they keep related files in
sync. Manual edits are useful for advanced customization, but every generated
copy and its source-of-truth must remain consistent.

### Manual user-level configuration

The persistent configuration is:

```text
~/.codex/codex_workflow/workflow_config.json
```

The current default snapshot is:

```json
{
  "schema_version": 2,
  "default_executor": "executor_luna",
  "default_executor_reasoning_effort": "xhigh",
  "max_concurrent_workers": 20,
  "max_executor_sol_instances": 1,
  "report_package_size": 250,
  "enabled_workers": [
    "executor_luna",
    "executor_sol",
    "tester",
    "doc-writer",
    "explorer"
  ]
}
```

When editing this file manually:

1. keep valid JSON and a supported schema;
2. set `default_executor` to `executor_luna` or `executor_terra` and keep it
   inside `enabled_workers`;
3. set `default_executor_reasoning_effort` to `high`, `xhigh`, or `max`;
4. keep `doc-writer` enabled because project installation depends on it;
5. keep worker names unique and backed by templates in
   `~/.codex/codex_workflow/templates/agents/`;
6. keep exactly one of `executor_luna` and `executor_terra` enabled as the
   default executor;
7. keep `max_executor_sol_instances` between zero and the concurrency limit.

After a direct edit, synchronize the effective configuration block in
`~/.codex/codex_workflow/heavy_route.md`, the active workflow TOMLs in
`~/.codex/agents/`, and the workflow-owned keys in `~/.codex/config.toml`.
Using `codex_workflow --configure` performs this synchronization and is less
error-prone.

The concurrency values must stay synchronized: the confirmed
`max_concurrent_workers` in `workflow_config.json` is also written to
`[features.multi_agent_v2].max_concurrent_threads_per_session` in
`~/.codex/config.toml`. The value `20` is only the current package default; it
must be replaced when the user selects another valid limit.

When worker definitions or platform settings change, open a new Codex session
so the updated settings are loaded.

### Tuning an individual worker

Active workers live in `~/.codex/agents/`. Their TOML files define persistent
role behavior. For example, an advanced user may add:

```toml
service_tier = "fast"
```

to an installed worker whose service supports that setting. Keep the role's
scope, reporting contract, and safety boundaries intact. Do not edit unrelated
worker files or replace an active worker with a repository-only file.

To add a custom worker, ask Codex to create a worker template consistent with
the existing role files, place the template under the workflow template area,
add its name to `enabled_workers`, and install the active TOML. A custom
research-oriented `investigator` can be useful for web research in a niche
project, but it should be enabled only when its role and concurrency cost are
understood.

### Tuning project personalization

The private source resource is:

```text
.codex_workflow_hidden_resource/personalization.md
```

It contains the confirmed Frontend Project Profile, Design Principles, and
Additional Workflow Decisions. Its decisions are materialized only inside the
marked personalization block in `AGENTS.md` (or the hidden entry point while
the project is disabled).

For manual changes, update the resource and its materialized marker together,
preserve the marker boundaries, and keep secrets or conversation logs out of
both files. Prefer `codex_workflow --personal`, which validates the three
sections and performs the materialization safely.

Do not put personalization in `agent_docs/`: those six files are durable
project context and are intentionally available to the normal workflow.

### Customizing routes and documentation

Advanced route changes belong in:

```text
~/.codex/codex_workflow/heavy_route.md
~/.codex/codex_workflow/medium_route.md
```

Possible customizations include:

- replacing `project_progress.md` with a dedicated codebase navigation or
  management tool for a very large repository;
- adding a project-specific worker and wiring its responsibility into the
  Heavy route;
- adapting the End-of-Session handoff in `end_of_session.md` to match the
  project's release or review practice.

Keep the route's ownership boundaries, worker limits, verification gates, and
main-agent ownership of the two session-state documents. After a route change,
verify that the effective configuration block and worker list still agree with
`workflow_config.json`.

## Part 4 — How the Heavy route works

The Heavy route is an orchestrated deployment-state workflow. It is selected
explicitly by the user; Light remains the default for small tasks. The Heavy
route does not mean that every prompt must spawn workers: common questions and
small tasks may still be handled directly by the main agent.

### Roles and ownership

The current enabled set is:

| Role | Responsibility | Can edit project source? |
| --- | --- | --- |
| Main agent | Chooses scope, plans, delegates, integrates, reviews critical boundaries, and owns status/handoff docs | Yes, under the user-approved task scope |
| Selected default executor (`executor_luna` or `executor_terra`) | Production implementation worker | Yes, within its work package |
| `executor_sol` | Complex core reasoning or fallback implementation | Yes, within its work package; limited to one active instance |
| `tester` | Independent focused tests and failure analysis | Test/fixture scope; production defects return to the executor |
| `doc-writer` | Verified durable architecture, structure, workflow, or usage documentation | Documentation scope, except main-owned status/handoff files |
| Explorer companion | Read-only context gathering and session-long supplementary research | No |

`executor_terra.toml` is distributed as a template and becomes active when it
is selected as the default executor. The active list, selected executor, and
limits come from `workflow_config.json` and are copied into the Heavy route's
effective-configuration block.

### Context loading and work-package flow

When Heavy is selected for a deployment-state task, the main agent:

1. reads the project entry point and the workflow's Heavy-route instructions;
2. initializes one read-only Explorer companion;
3. loads the bounded foundational project context: overview, structure,
   progress, and latest-session handoff, then reconciles the remaining relevant
   documents;
4. defines a bounded plan, acceptance criteria, ownership, protected areas,
   dependencies, and verification gates;
5. sends self-contained work packages to only the enabled workers needed for
   the task.

Each work package contains the task identity, outcome, ownership, source paths,
completion criteria, validation, protected areas, and return format. Normal
initial capsules are concise, follow-ups contain only new evidence, and final
reports are limited by `report_package_size`.

The normal implementation and verification loop is:

```text
User selects Heavy route
        │
        ▼
Main agent loads project context and initializes read-only Explorer
        │
        ▼
Main agent creates bounded package(s) for the selected default executor or executor_sol
        │
        ▼
Executor implements one coherent increment and self-validates
        │
        ▼
Tester independently runs focused checks when testing is warranted
        │
        ├── proof  ──► main agent reviews and integrates
        ├── defect ─► same executor receives a bounded repair delta
        ├── blocker ─► main agent re-scopes or requests a decision
        └── replacement/takeover ─► recovery path after repeated evidence loss
        │
        ▼
Doc-writer records verified durable documentation when required
        │
        ▼
Main agent performs critical integration review and session handoff
```

The tester is normally started after the executor hands off a completed
increment. A production defect goes back to that same executor; a test or
fixture defect stays with the tester. Repair loops respond to new evidence and
do not repeat work merely to increase activity.

### Concurrency and communication controls

The current configuration permits at most five concurrent child workers and
at most one `executor_sol` instance. The Explorer companion does not consume a
worker slot. The main agent must not exceed the enabled-worker list or these
limits.

Worker communication is event-driven. `proof`, `defect`, `blocker`, and
`replacement/takeover` events are used when evidence changes coordination,
risk, scope, or the next action. A worker that returns no concrete evidence
gets one short retry; repeated evidence-free work triggers replacement or an
explicit main-agent takeover with an honest report.

Workers must not edit Git state or the main-owned
`agent_docs/project_progress.md` and `agent_docs/latest_session_work.md`. The
main agent owns those files and performs the final integration review. The
Explorer remains read-only even though it can inspect adjacent context.

### Cross-session continuity

`project_progress.md` carries the active deployment plan and status.
`latest_session_work.md` carries the latest handoff and unfinished work. They
let a later session resume without sending the entire previous conversation to
every worker.

When the user sends `end this session`, Heavy collects worker checkpoints when
needed while Medium skips that worker-only step. Both routes verify the final
state, complete warranted durable documentation, and run the Explorer closure
audit when applicable. If the deployment plan is complete, both
`project_progress.md` and `latest_session_work.md` are cleared but kept as
empty framework files; if work remains, they are updated with the next
handoff. Meaningful project changes are committed according to the installed
handoff procedure.

## Part 5 — Component hierarchy and ownership

The original design grouped the system into five logical blocks across two
geographical levels. That model remains useful, but some paths need a precise
distinction: `agent_docs/` is project documentation, while personalization is
private under `.codex_workflow_hidden_resource/`; worker TOMLs are active
runtime definitions, while `workflow_config.json` is their persistent
configuration source.

The five blocks are:

### 1. Workflow runtime — user level

Location: `~/.codex/`

- `~/.codex/agents/` contains active worker TOMLs. The current active set is
  `executor_luna`, `executor_sol`, `tester`, `doc-writer`, and `explorer`.
- `~/.codex/codex_workflow/heavy_route.md` defines Heavy orchestration,
  delegation, limits, repair loops, and ownership.
- `~/.codex/codex_workflow/medium_route.md` defines the full workflow when no
  subagents are used.
- `~/.codex/codex_workflow/explorer_companion.md` defines the read-only
  Explorer's lifecycle and boundary.
- `~/.codex/codex_workflow/end_of_session.md` defines the shared handoff.

This block is the reusable execution machinery. It is shared by projects and
does not contain project-specific decisions.

### 2. Workflow integration — project level

Location: the current project directory

- `AGENTS.md` is the active project entry point and contains the workflow
  instructions materialized for this project.
- `agent_docs/` contains the six-document Project Documentation Framework.
- `.codex_workflow_hidden_resource/.AGENTS.md` is the same entry point in its
  disabled state and must not coexist with root `AGENTS.md`.

This block connects the shared runtime to one project. Its project documents
are durable context, not private configuration.

### 3. Configuration — user level

Primary resource:

```text
~/.codex/codex_workflow/workflow_config.json
```

The resource currently contains:

1. `default_executor`: currently `executor_luna`;
2. `default_executor_reasoning_effort`: currently `xhigh`;
3. `max_concurrent_workers`: currently `20`;
4. `max_executor_sol_instances`: currently `1`;
5. `enabled_workers`: currently `executor_luna`, `executor_sol`, `tester`,
   `doc-writer`, and `explorer`;
6. `report_package_size`: currently `250` words.

Related configuration surfaces are:

- `~/.codex/agents/*.toml`: materialized active worker definitions;
- `~/.codex/config.toml`: workflow-owned Codex platform settings, merged into
  the user's existing configuration without replacing unrelated settings;
- `~/.codex/codex_workflow/templates/agents/`: all distributed worker
  templates, including the alternate `executor_terra`.

`workflow_config.json` is the source of the workflow-level values. The route
snapshot, active worker files, and platform settings are synchronized outputs;
they must not silently disagree with it.

### 4. Personalization — project level

Private resource:

```text
.codex_workflow_hidden_resource/personalization.md
```

It contains the confirmed project-scoped decisions:

1. **Frontend Project Profile** — for example, a deliberate reduced frontend
   verification profile;
2. **Design Principles** — project-specific design and engineering rules;
3. **Additional Workflow Decisions** — other confirmed project instructions.

The resource is intentionally hidden from ordinary project context. Its
effective instructions are materialized between the personalization markers
in `AGENTS.md` or in the hidden disabled entry point. It is not stored in
`agent_docs/`, and `agent_docs/` should not be used as a substitute for it.

### 5. Guidance and lifecycle control — user level

Location: `~/.codex/codex_workflow/`

- `user_AGENTS.md` contains the workflow marker, installed version marker, and
  exact command prompts for `--install`, `--update`, `--check-update`,
  `--configure`, `--personal`, `--disable`, and `--enable`.
- `install.md`, `configuration_guide.md`, and `personalization_guide.md`
  describe bootstrap, configuration, and personalization.
- `update.md`, `disable.md`, and `enable.md` describe update and activation
  lifecycle operations.
- `check_update.md` describes the read-only Release version check.
- `VERSION` identifies the installed workflow version.
- `templates/` stores the project entry-point, worker, and project-document
  templates used for installation and update.
- `.source_backup/` keeps a complete release source copy for repair and
  recovery; update-time `.backups/` preserve replaced installed state.

This block is the command and lifecycle control plane. It tells Codex how to
perform operations; it is not itself the project context or the active worker
execution layer.

These five blocks are logical ownership boundaries, not five disjoint
directories. For example, `~/.codex/codex_workflow/` hosts routes, guidance,
configuration, templates, and backups. The distinction is about who owns the
data and how it is consumed:

```text
User level:    shared runtime + global configuration + lifecycle guidance
                    │
                    │ materialized into the current project
                    ▼
Project level: entry point + six durable documents + private personalization
```
