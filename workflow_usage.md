# codex_workflow — Workflow Usage Guide

`codex_workflow` is a modular Codex workflow with explicit responsibility
boundaries, persistent project documentation, shared user-level runtime files,
and conservative lifecycle operations.

This guide is organized into five parts:

1. command prompts and route selection;
2. the installed-file map;
3. scripted configuration and customization;
4. the Heavy-route execution model;
5. the component hierarchy and ownership model.

## Part 1 — Command prompts and everyday use

### First-time bootstrap

Open Codex from the project directory and send this prompt:

```text
Download and extract the latest GitHub Release from https://github.com/viettran-edgeAI/codex_workflow/releases. Then read the bundled `codex_workflow/bootstrap.md` and follow it exactly.
```

The release package is a universal ZIP for Linux, macOS, and Windows. Its
installation guide invokes the bundled lifecycle CLI, which owns validation,
rendering, backups, project initialization, and rollback. After the first
installation, start a new Codex session so the newly installed user
instructions are loaded. Python 3.10 or newer is required.

The bootstrap installs the user-level workflow and the current project. It
does not ask configuration or personalization questions. Those are explicit
follow-up commands. It also adds the workflow-owned project paths to
`.gitignore` and removes a project-level `Codex_Workflow/` extraction directory
once the installation transaction succeeds.

### Exact command prompts

Send each command as its own prompt. The installed lifecycle CLI performs the
validated filesystem operation directly.

#### `codex_workflow --configure`

Interactively change the persistent user-level workflow configuration. The
command displays a menu containing every setting below, with **Exit** at the
bottom. Choose one setting at a time; after a change, the menu is displayed
again until **Exit** is selected.

- default executor (`executor_luna` or `executor_terra`);
- default executor reasoning effort (`high`, `xhigh`, or `max`);
- maximum concurrent workers;
- maximum concurrent `executor_sol` workers;
- final-report package size;
- End-of-Session recent-context turns.

The command shows the current values, builds a complete new JSON snapshot, and
then synchronizes the Heavy route,
End-of-Session spawn contract, all workflow worker TOMLs, and workflow-owned
Codex platform settings. It does not change project personalization or project
documents.

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

Install the workflow in the current project after the user-level workflow has
already been bootstrapped:

- creates or preserves the project `AGENTS.md` entry point;
- imports a pre-existing project `AGENTS.md` into the dedicated project-local
  region instead of semantically merging it;
- creates missing files in `agent_docs/` from the six project-document
  templates;
- initializes only newly created documentation with `doc-writer`;
- creates the default hidden personalization resource when missing;
- reuses the installed user-level configuration as a read-only source.

It does not reinstall or modify any user-level payload under `~/.codex/`, reset
existing project documents, or ask configuration and personalization
questions. If the workflow already has an active or disabled project entry
point, the command makes no changes and instructs the user to run
`codex_workflow --enable`.

#### `codex_workflow --update`

Update the installed workflow and the recognized current project from a GitHub
Release asset. The command queries the GitHub Releases API, selects the latest
eligible semantic-versioned release with the matching ZIP and checksum,
downloads the asset, verifies it, and extracts it into a temporary directory.
It never clones or pulls the repository.

The update replaces the workflow configuration and distributed worker TOMLs
from the incoming package. It preserves project personalization, project-local
instructions, project documents, unrelated Codex settings, source backups, and
the project's enabled or disabled state. It stops only on marker drift or
legacy edits requiring a one-time reviewed migration.

#### `codex_workflow --check-update`

Run an explicit read-only release check. It always queries the available
installable releases, regardless of the automatic-check setting, and reports
every version newer than the installed one with a compact summary of each
release's notes. It does not download or change files.

#### `codex_workflow --remove`

Remove the installed workflow in two phases. The first invocation creates a
read-only destructive summary and warns the user. Only after one explicit
second confirmation does the lifecycle CLI delete the project workflow entry
point, project workflow resource, user-managed workflow region, workflow-owned
Codex settings and workers, and the complete installed runtime including
backups. It preserves `agent_docs/` and unrelated user-level content. A
non-affirmative response performs no changes.

#### Automatic update check

At the start of each new session, Codex runs the lifecycle CLI's read-only
`auto-check-update` command once. When enabled, it compares the installed
version with the highest usable GitHub Release and reports an available update.
It stays quiet when the workflow is current or the check is disabled. The
package default is disabled.

Send `codex_workflow --enable_auto_update` to explicitly enable the
session-start check, or `codex_workflow --disable_auto_update` to disable it
again. Each command changes only the mutable installed configuration. The
former `codex_workflow --disable_auto_check_update` prompt remains a
compatibility alias.

#### `codex_workflow --disable`

Disable the workflow for the current project by moving the active entry point:

```text
AGENTS.md -> .codex_workflow_hidden_resources/.AGENTS.md
```

The contents, personalization resource, project documents, and user-level
workflow remain intact. The operation is a safe no-op when the project is
already disabled.

#### `codex_workflow --enable`

Re-enable a disabled project by moving the entry point back:

```text
.codex_workflow_hidden_resources/.AGENTS.md -> AGENTS.md
```

This changes only the active/disabled entry-point state. It does not reread or
reapply configuration or personalization.

### Route selection and session closure

There are three execution routes:

- **Light route** — the default; the main agent works alone with minimal
  workflow overhead.
- **Medium route** — the main agent performs implementation and verification;
  only Explorer and the dedicated handoff worker are used.
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

A fresh Luna xhigh worker receives the configured number of recent turns and
owns the entire End-of-Session handoff.

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
├── agents/                                # all distributed workflow worker TOMLs
│   ├── executor_luna.toml
│   ├── executor_terra.toml
│   ├── executor_sol.toml
│   ├── tester.toml
│   ├── doc-writer.toml
│   ├── explorer.toml
│   └── end_of_session.toml
└── codex_workflow/
    ├── VERSION                             # installed workflow version
    ├── user_AGENTS.md                      # managed command marker and command prompts
    ├── workflow_config.json                # persistent workflow configuration
    ├── workflow.py                         # validated lifecycle CLI
    ├── runtime/                            # validation, rendering, release, and transaction modules
    ├── resources/                          # immutable package defaults
    │   ├── personalization.md
    │   └── workflow_config.default.json
    ├── install_state.json                  # workflow ownership and installed-state manifest
    ├── heavy_route.md                      # Heavy-route orchestration rules
    ├── medium_route.md                     # Medium-route rules
    ├── explorer_companion.md               # read-only Explorer lifecycle and boundaries
    ├── end_of_session.md                   # shared handoff spawn contract
    ├── bootstrap.md                        # initial user/project bootstrap procedure
    ├── install.md                          # project-only installation procedure
    ├── update.md                           # Release-based update procedure
    ├── check_update.md                     # explicit read-only release check
    ├── remove.md                            # two-phase removal procedure
    ├── enable_auto_update.md               # enable automatic session check
    ├── disable_auto_update.md              # disable automatic session check
    ├── disable_auto_check_update.md        # legacy disable alias
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
├── .gitignore                               # workflow-owned project paths are ignored
├── agent_docs/
│   ├── project_overview.md
│   ├── project_core_tech.md
│   ├── project_structure.md
│   ├── project_progress.md
│   ├── project_diary.md
│   └── latest_session_work.md
└── .codex_workflow_hidden_resources/
    ├── personalization.md                  # project-scoped private resource
    ├── state.json                          # project entry-format and activation state
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
- `project_progress.md` — concise overall progress and current milestone;
- `project_diary.md` — durable decisions, discarded approaches, and lessons;
- `latest_session_work.md` — detailed current state, evidence, unfinished work,
  and continuation point.

## Part 3 — Scripted configuration and customization

Command prompts select an operation. The lifecycle CLI validates and
materializes all generated surfaces from their source resources.

### User-level configuration

The persistent configuration is:

```text
~/.codex/codex_workflow/workflow_config.json
```

This mutable installed state is distinct from the immutable package default at
`~/.codex/codex_workflow/resources/workflow_config.default.json`. Bootstrap and
update load the incoming package default and replace the mutable workflow
configuration. The project entry point's enabled/disabled state is preserved
separately.

The current default snapshot is:

```json
{
  "schema_version": 3,
  "default_executor": "executor_luna",
  "default_executor_reasoning_effort": "xhigh",
  "auto_check_update": false,
  "end_of_session_context_turns": 200,
  "max_concurrent_workers": 20,
  "max_executor_sol_instances": 1,
  "report_package_size": 250,
  "enabled_workers": [
    "executor_luna",
    "executor_sol",
    "tester",
    "doc-writer",
    "explorer",
    "end_of_session"
  ]
}
```

The configuration contract is:

1. keep valid JSON and a supported schema;
2. set `default_executor` to `executor_luna` or `executor_terra` and keep it
   inside `enabled_workers`;
3. set `default_executor_reasoning_effort` to `high`, `xhigh`, or `max`;
4. keep `auto_check_update` boolean; it defaults to `false`;
5. keep `end_of_session_context_turns` a positive integer; it defaults to `200`;
6. keep `doc-writer` enabled because project installation depends on it and
   keep `end_of_session` enabled because both deployment routes require it;
7. keep worker names unique and backed by templates in
   `~/.codex/codex_workflow/templates/agents/`;
8. keep exactly one of `executor_luna` and `executor_terra` enabled as the
   default executor;
9. keep `max_executor_sol_instances` between zero and the concurrency limit.

Do not edit generated surfaces directly. `codex_workflow --configure`
synchronizes the Heavy snapshot, handoff contract, all worker TOMLs, and
workflow-owned `config.toml` keys.

The concurrency values must stay synchronized: the confirmed
`max_concurrent_workers` in `workflow_config.json` is also written to
`[features.multi_agent_v2].max_concurrent_threads_per_session` in
`~/.codex/config.toml`. The value `20` is only the current package default; it
must be replaced when the user selects another valid limit.

When worker definitions or platform settings change, open a new Codex session
so the updated settings are loaded.

### Tuning an individual worker

All distributed workers live in `~/.codex/agents/` and are generated from
templates. The `enabled_workers` configuration controls which materialized
workers the workflow may create and use.
Advanced changes belong in the owned template before reconfiguration. For
example, a template may add:

```toml
service_tier = "fast"
```

to an installed worker whose service supports that setting. Keep the role's
scope, reporting contract, and safety boundaries intact. Do not edit unrelated
worker files or replace a materialized worker with a repository-only file.

To add a custom worker, ask Codex to create a worker template consistent with
the existing role files, place the template under the workflow template area,
add its name to `enabled_workers`, and install the active TOML. A custom
research-oriented `investigator` can be useful for web research in a niche
project, but it should be enabled only when its role and concurrency cost are
understood.

### Tuning project personalization

The private source resource is:

```text
.codex_workflow_hidden_resources/personalization.md
```

It contains the confirmed Frontend Project Profile, Design Principles, and
Additional Workflow Decisions. Its decisions are materialized only inside the
marked personalization block in `AGENTS.md` (or the hidden entry point while
the project is disabled).

Do not edit its materialized marker directly. `codex_workflow --personal`
validates a complete candidate and atomically updates the resource and generated
region while preserving project-local instructions.

Do not put personalization in `agent_docs/`: those six files are durable
project context and are intentionally available to the normal workflow.

### Customizing routes and documentation

Advanced route changes belong in a maintained source package or fork, not in an
installed generated copy that update will replace:

```text
~/.codex/codex_workflow/heavy_route.md
~/.codex/codex_workflow/medium_route.md
```

Possible customizations include:

- replacing `project_progress.md` with a dedicated codebase navigation or
  management tool for a very large repository;
- adding a project-specific worker and wiring its responsibility into the
  Heavy route;
- adapting the `end_of_session` worker instruction to the project's release or
  review practice while keeping `end_of_session.md` as the spawn contract.

Keep the route's ownership boundaries, worker limits, verification gates, and
dedicated handoff ownership of the two session-state documents. After a route
change, verify that the effective configuration block and worker list still
agree with `workflow_config.json`.

## Part 4 — How the Heavy route works

The Heavy route is an orchestrated deployment-state workflow. It is selected
explicitly by the user; Light remains the default for small tasks. The Heavy
route does not mean that every prompt must spawn workers: common questions and
small tasks may still be handled directly by the main agent.

### Roles and ownership

The current enabled set is:

| Role | Responsibility | Can edit project source? |
| --- | --- | --- |
| Main agent | Chooses scope, plans, delegates, integrates, and reviews critical boundaries during normal execution | Yes, under the user-approved task scope |
| Selected default executor (`executor_luna` or `executor_terra`) | Production implementation worker | Yes, within its work package |
| `executor_sol` | Complex core reasoning or fallback implementation | Yes, within its work package; limited to one active instance |
| `tester` | Independent focused tests and failure analysis | Test/fixture scope; production defects return to the executor |
| `doc-writer` | Verified durable architecture, structure, workflow, or usage documentation | Documentation scope, except shared status/handoff files |
| Explorer companion | Read-only context gathering and session-long supplementary research | No |
| `end_of_session` | Complete Medium/Heavy handoff, status documents, and Git closure | Documentation and Git state during an invoked handoff |

`executor_terra.toml` is materialized alongside the other worker definitions;
it becomes the selected default executor only when configured as such. The
enabled list, selected executor, and limits come from `workflow_config.json`
and are copied into the Heavy route's
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

Each work package contains the task identity, outcome, ownership, relevant
decision context, source paths, completion criteria, validation, protected
areas, and return format. The default executor also receives a recommended
approach and rationale; `executor_sol` receives constraints without a proposed
solution. Normal initial capsules are concise, follow-ups contain only new
evidence, and final reports are limited by `report_package_size`.

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
Main agent performs critical integration review
        │
        ▼
On `end this session`, a fresh Luna xhigh worker receives recent context and owns the handoff
```

The tester is normally started after the executor hands off a completed
increment. A production defect goes back to that same executor; a test or
fixture defect stays with the tester. Repair loops respond to new evidence and
do not repeat work merely to increase activity.

### Concurrency and communication controls

The current configuration permits at most twenty concurrent child workers and
at most one `executor_sol` instance. Explorer is reported as a companion rather
than a task worker, but its live thread consumes platform capacity. Heavy keeps
one child-agent slot available for the fresh End-of-Session worker and must not
exceed the enabled-worker list or configured limits.

Worker communication is event-driven. `proof`, `defect`, `blocker`, and
`replacement/takeover` events are used when evidence changes coordination,
risk, scope, or the next action. A worker that returns no concrete evidence
gets one short retry; repeated evidence-free work triggers replacement or an
explicit main-agent takeover with an honest report.

Task workers must not edit Git state or the shared status documents. The main
agent owns those surfaces during normal execution; `end_of_session` alone owns
them during an invoked handoff. Explorer remains read-only.

### Cross-session continuity

`project_progress.md` carries only the goal, overall progress, current position,
and next milestone. `latest_session_work.md` carries the detailed current state,
verification, blockers, and exact continuation point.

When the user sends `end this session`, either route creates a fresh
`end_of_session` worker with the configured finite `fork_turns` value, `200` by
default. This preserves its Luna xhigh model while providing recent session
context. Its instruction owns checkpoint collection when needed, evidence
reconciliation, durable handoff documents, compact closing checks, Git commit,
and the final report. Explorer has no closure responsibility. The main agent
waits and relays the result.

## Part 5 — Component hierarchy and ownership

The original design grouped the system into five logical blocks across two
geographical levels. That model remains useful, but some paths need a precise
distinction: `agent_docs/` is project documentation, while personalization is
private under `.codex_workflow_hidden_resources/`; worker TOMLs are materialized
runtime definitions, while `workflow_config.json` is their persistent
configuration source.

The five blocks are:

### 1. Workflow runtime — user level

Location: `~/.codex/`

- `~/.codex/agents/` contains all distributed worker TOMLs. The current
  enabled set is `executor_luna`, `executor_sol`, `tester`, `doc-writer`,
  `explorer`, and `end_of_session`; `executor_terra` remains available as the
  alternate default executor.
- `~/.codex/codex_workflow/heavy_route.md` defines Heavy orchestration,
  delegation, limits, repair loops, and ownership.
- `~/.codex/codex_workflow/medium_route.md` defines main-agent execution with
  only Explorer and End-of-Session subagent exceptions.
- `~/.codex/codex_workflow/explorer_companion.md` defines the read-only
  Explorer's lifecycle and boundary.
- `~/.codex/codex_workflow/end_of_session.md` defines the shared spawn contract;
  `end_of_session.toml` contains the complete handoff procedure.

This block is the reusable execution machinery. It is shared by projects and
does not contain project-specific decisions.

### 2. Workflow integration — project level

Location: the current project directory

- `AGENTS.md` is the active project entry point and contains the workflow
  instructions materialized for this project.
- `agent_docs/` contains the six-document Project Documentation Framework.
- `.codex_workflow_hidden_resources/.AGENTS.md` is the same entry point in its
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
3. `auto_check_update`: currently `false`;
4. `end_of_session_context_turns`: currently `200`;
5. `max_concurrent_workers`: currently `20`;
6. `max_executor_sol_instances`: currently `1`;
7. `enabled_workers`: currently `executor_luna`, `executor_sol`, `tester`,
   `doc-writer`, `explorer`, and required `end_of_session`;
8. `report_package_size`: currently `250` words.

Related configuration surfaces are:

- `~/.codex/codex_workflow/resources/workflow_config.default.json`: immutable
  package defaults and migration fallback;
- `~/.codex/agents/*.toml`: materialized definitions for all distributed workers;
- `~/.codex/config.toml`: workflow-owned Codex platform settings, merged into
  the user's existing configuration without replacing unrelated settings;
- `~/.codex/codex_workflow/templates/agents/`: all distributed worker
  templates, including the alternate `executor_terra`.

`workflow_config.json` is the source of the workflow-level values. The route
snapshot, worker files, and platform settings are synchronized outputs;
they must not silently disagree with it.

### 4. Personalization — project level

Private resource:

```text
.codex_workflow_hidden_resources/personalization.md
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

- `user_AGENTS.md` contains the workflow marker, installed version marker,
  session-start update-check instruction, and exact command prompts for
  `--install`, `--update`, `--remove`, `--enable_auto_update`,
  `--disable_auto_update`, `--configure`, `--personal`, `--disable`, and
  `--enable`.
- `bootstrap.md`, `install.md`, `configuration_guide.md`, and
  `personalization_guide.md` describe initial bootstrap, project installation,
  configuration, and personalization.
- `update.md`, `disable.md`, and `enable.md` describe update and activation
  lifecycle operations.
- `remove.md` describes the destructive two-phase removal procedure.
- `enable_auto_update.md` and `disable_auto_update.md` describe the explicit
  update-check controls; `disable_auto_check_update.md` remains a legacy alias.
- `workflow.py` and `runtime/` implement validated lifecycle operations.
- `VERSION` identifies the installed workflow version.
- `templates/` stores the project entry-point, worker, and project-document
  templates used for installation and update.
- `.source_backup/` keeps a complete release source copy for repair and
  recovery; update-time `.backups/` preserve replaced installed state.

This block is the command and lifecycle control plane. Guides define intent and
the runtime performs deterministic mutations. It is not project context or the
worker execution layer.

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
