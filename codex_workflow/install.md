# Workflow Installation

Use this procedure only to install the already-bootstrapped workflow into the
current project. Do not manually copy or merge workflow files, and do not
modify or reinstall anything under `~/.codex/`.

Python 3.10 or newer is required. On Windows, use the equivalent `py -3.10`
invocation and native paths.

## Existing project installation

Check the current project's active `AGENTS.md` and disabled
`.codex_workflow_hidden_resources/.AGENTS.md` entry points. If either is a
recognized codex_workflow entry point, do not install or modify anything.
Tell the user to run:

```text
codex_workflow --enable
```

This instruction applies whether the recognized entry point is active or
disabled.

## Install the current project

Use the installed CLI:

```text
python3 ~/.codex/codex_workflow/workflow.py install \
  --project <project>
```

The command reads templates from the existing user-level bootstrap but changes
only the current project. It creates the project `AGENTS.md`, missing files in
the `agent_docs/` documentation scaffold, the hidden personalization and state
files, and other project-level assets. It imports an existing unrecognized
project `AGENTS.md` verbatim into the project-local marker region and adds the
workflow-owned project paths to `.gitignore` without changing unrelated rules.

It does not rewrite the shared user-level runtime, configuration, user
instructions, source backup, or worker TOMLs under `~/.codex/`. Stop and report
the error if the initial user-level bootstrap is missing.

## Required documentation action

The result always contains one required `doc-writer` action. Spawn it with
`agent_type="doc-writer"`, `task_name="install_docs"`, and
`fork_turns="none"`. Pass the project root and returned `files`, `framework`, and
`required_context_files` lists. Initialize only listed new documents, remove
their bootstrap markers, and preserve existing documents. Populate newly created
`project_structure.md`, `project_overview.md`, and `project_core_tech.md` with
verified project evidence. If `files` is empty, perform only a read-only
framework completeness check. An empty project is valid; explicitly record that
project context was unavailable and leave deployment status empty when no plan
exists.

Installation is incomplete if the required worker cannot run or fails. Do not
silently perform its work in the main thread.
