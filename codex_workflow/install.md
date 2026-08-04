# Workflow Installation

This document defines installation at two scopes:

- User-level: `~/.codex/`, installed once per user environment.
- Project: the current project, installed once per project.

Do not inspect or edit the project's source code files during installation.
Source paths below are relative to the cloned workflow repository root.

## Installation modes

- The README installation prompt runs the user-level phase and then the project
  phase for the current project.
- `codex_workflow --install` runs only the project phase. It assumes the user-level
  phase is already complete.
- `codex_workflow --update` is handled by `update.md`: update the user-level phase
  first, then update the recognized current project.

## Path handling

Paths use `/` as a platform-neutral separator. Adapt filesystem commands to the
current operating system and shell. Resolve these directories to the current
user's home directory:

```text
~/.codex/
~/.codex/codex_workflow/
~/.codex/agents/
```

Do not treat the displayed separator or `~` as literal requirements on every
platform.

## Release and project identity

The source package version is the `codex-workflow-version` marker in
`codex_workflow/user_AGENTS.md`. It must match the marker in `README.md`.
Stop and report an inconsistent release if they differ.

The installed user-level version is the `codex-workflow-version` marker in:

```text
~/.codex/AGENTS.md
```

The project workflow marker is:

```text
<!-- codex-workflow-id: viettran-edgeAI/codex_workflow -->
```

If a project `AGENTS.md` contains this exact marker, it is a recognized
installation. Project updates may replace it after protected content has been
captured. If the marker is absent, use the conflict handling below and do not
transfer existing personalization automatically.

## 1. User-level installation — once per user environment

Run this phase during the README installation prompt or an explicit workflow
update. Never run it for `codex_workflow --install`.

### 1.1 User-level workflow bundle

Copy the six runtime documents into the Codex user directory:

```text
codex_workflow/install.md
codex_workflow/personalization.md
codex_workflow/update.md
codex_workflow/heavy_route.md
codex_workflow/medium_route.md
codex_workflow/explorer_companion.md
→ ~/.codex/codex_workflow/
```

This creates or replaces the workflow-owned directory
`~/.codex/codex_workflow/`. Replace the workflow-owned runtime documents so the
installed set matches the source set. Report each replacement.

### 1.2 User-level agent definitions

Copy every agent definition:

```text
codex_workflow/agents/*.toml
→ ~/.codex/agents/
```

Overwrite same-named destination files and report each overwrite. Preserve
unrelated agent definitions already present in `~/.codex/agents/`.

### 1.3 Codex multi-agent configuration

Check:

```text
~/.codex/config.toml
```

If the environment uses `/.codex` as its Codex directory, check:

```text
/.codex/config.toml
```

Add the following configuration if it is not already present. If the section
exists, add only missing keys and preserve existing values:

```toml
[features.multi_agent_v2]
hide_spawn_agent_metadata = false
tool_namespace = "agents"
```

### 1.4 User-level AGENTS.md

Copy:

```text
codex_workflow/user_AGENTS.md
→ ~/.codex/AGENTS.md
```

If `~/.codex/AGENTS.md` contains the exact user-level workflow marker, update the
workflow-owned version and `## Workflow Update` section while preserving
unrelated user-level instructions. If it lacks the marker, do not overwrite it
automatically; ask whether to replace or merge it.

### 1.5 Verify user-level installation

Verify that:

- `~/.codex/AGENTS.md` contains the user-level workflow marker and source version.
- `~/.codex/codex_workflow/` contains the six runtime documents from
  `codex_workflow/`, including `install.md`, `personalization.md`, and
  `update.md`.
- Every TOML in `codex_workflow/agents/` exists under `~/.codex/agents/`.
- The required multi-agent configuration is present.
- No unrelated user-level files were modified.

Report installed files, skipped files, conflicts, replacements, and unresolved
issues.

## 2. Project installation — `codex_workflow --install`

This phase must not reinstall or replace anything under `~/.codex/`. It only
creates the default project framework.

### 2.1 Check the user-level installation

Require these existing user-level files:

- `~/.codex/AGENTS.md` with the user-level workflow marker;
- `~/.codex/codex_workflow/`;
- `~/.codex/agents/` with the workflow agent definitions.

If they are missing, stop and tell the user to run the README installation
prompt first. Do not silently perform user-level installation from `--install`.

### 2.2 Project AGENTS.md

Copy the default project instructions:

```text
codex_workflow/AGENTS.md
→ AGENTS.md
```

If `AGENTS.md` already contains the project workflow marker, report that the
workflow is already installed and do not replace it during `--install`. If it
exists without the marker, ask whether to replace, merge, or skip.

### 2.3 Main project documentation

Create `agent_docs/` only if it is missing. Do not overwrite an existing
`agent_docs/` directory.

Create these six documents if they do not already exist:

- `agent_docs/project_overview.md`
- `agent_docs/project_core_tech.md`
- `agent_docs/project_structure.md`
- `agent_docs/project_progress.md`
- `agent_docs/project_diary.md`
- `agent_docs/latest_session_work.md`

Do not ask personalization questions or modify user-level files during this
command. The project starts with the default workflow configuration. A later
personalization phase may create `agent_docs/workflow_personalization.md`.

### 2.4 Verify project installation

Verify that:

- `AGENTS.md` exists in the project root with the project marker.
- The six main documents exist under `agent_docs/`.
- No user-level bundle, agent definition, or unrelated project file was modified.

Report created, skipped, conflicting, and unresolved files.

## 3. Personalization after initial installation or update

Read and follow:

```text
~/.codex/codex_workflow/personalization.md
```

This phase is part of the initial README installation and workflow update. It
is not part of the minimal `codex_workflow --install` command.

The personalization procedure owns `agent_docs/workflow_personalization.md`,
the configuration questions, and their application to `AGENTS.md`, routes, and
agent TOML files. Do not ask again for a decision already recorded in that
project file.

For a recognized update, read and retain the current `## Project Context` body
before replacing `AGENTS.md`. Reapply it and the complete personalization
record to the new project instructions. Remove obsolete project-local
`agent_docs/workflow/` only after the user-level bundle is verified.

## 4. Finish installation

Report the user-level and project scopes separately, including versions,
personalization status, conflicts, and unresolved issues. Instruct the user to
restart Codex after user-level agent definitions change.

When running from a temporary clone of the workflow repository, delete only
that temporary package and its presentation files after verification:

- `codex_workflow/`
- `README.md`
- `illustration.png`

Do not delete `agent_docs/`, `AGENTS.md`, the personalization record, or any
other project file. A normal `codex_workflow --install` run has no temporary
package to delete.
