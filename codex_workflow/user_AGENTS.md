<!-- codex-workflow-user-id: viettran-edgeAI/codex_workflow -->
<!-- codex-workflow-version: 1.0.0 -->
# AGENTS.md

## Workflow Update

This is the user-level control plane for the Codex workflow. The authoritative
installed workflow version is stored in:

```text
~/.codex/codex_workflow/VERSION
```

The `codex-workflow-version` marker in this file is synchronized metadata for
compatibility and human inspection.

When the user's trimmed message is exactly:

```text
codex_workflow --update
```

read and follow:

```text
~/.codex/codex_workflow/update.md
```

Update the user-level workflow bundle and agent definitions first, then update the
current project and reapply its `agent_docs/workflow_personalization.md` when it
exists.

When the user's trimmed message is exactly:

```text
codex_workflow --install
```

read and follow the project-installation section of:

```text
~/.codex/codex_workflow/install.md
```

This command assumes the user-level workflow is already installed. It must only
create the current project's default `AGENTS.md` and main `agent_docs/`
framework. It must not reinstall the user-level bundle, agent definitions, or
user-level Codex configuration.
