# Workflow Setup Guide

This is a task to set up a custom Codex workflow for the current project. Do not inspect or edit the project's source code files during this process.

If the directory has another name or location, use its actual path instead.

## Path handling

Paths in this workflow use `/` as a platform-neutral separator.

When executing filesystem operations, automatically adapt paths and commands to the current operating system and shell.

For example:

```text
agent_docs/workflows/heavy_route.md
```

represents the same logical location regardless of platform.

For the Codex user-agent directory:

```text
~/.codex/agents/
```

Resolve it to the appropriate user-home path on the current system.

Do not treat the path separator shown in this guide as a literal requirement.

## 1. Install the default workflow

### 1.1 Main-agent instructions

Copy:

```text
codex_workflows/AGENTS.md
```

to:

```text
AGENTS.md
```

in the current project root.

If `AGENTS.md` already exists, do not overwrite it automatically. Ask the user whether to replace it, merge the workflow instructions into it, or skip this step.

### 1.2 Project documentation

Create:

```text
agent_docs/
agent_docs/workflows/
```

Initialize the main project documents required by `AGENTS.md` inside:

```text
agent_docs/
```

Do not overwrite existing project documents without explicit user approval.

### 1.3 Workflow routes

Copy:

```text
codex_workflows/heavy_route.md
→ agent_docs/workflows/heavy_route.md

codex_workflows/medium_route.md
→ agent_docs/workflows/medium_route.md
```

If a destination file already exists, ask before replacing it.

### 1.4 Custom subagents

Create the Codex user-agent directory if it does not already exist:

```text
~/.codex/agents/
```

Copy these agent definitions into it:

```text
doc-writer.toml
tester.toml
executor_luna.toml
executor_sol.toml
```

Do not overwrite an existing agent definition without explicit user approval.

### 1.5 Verify installation

Verify that:

* `AGENTS.md` exists in the project root.
* Required project documents exist under `agent_docs/`.
* `heavy_route.md` and `medium_route.md` exist under `agent_docs/workflows/`.
* All four custom agent definitions exist under the Codex user-agent directory.
* No unrelated project source files were modified.

Report installed files, skipped files, conflicts, and unresolved issues.

## 2. Configure the project

Read all `.md` and `.toml` files in the `codex_workflows/` after installation. 
Ask the following questions one at a time.

### Core design principles

Ask:

> Would you like to define the work style and core design principles for this project?

This is optional.

Provide a few examples if useful, such as modularity, dependency limits, API stability, preferred languages, testing requirements, or project-specific constraints.

If the user provides instructions, add them under:

```text
## Core Design Principles
```

in the project-level `AGENTS.md`.

Preserve existing project-specific instructions.

### Power profile

Explain that the default Heavy route is configured to conserve ChatGPT Plus usage.

Ask whether the user wants to enable any of these options:

1. Allow more than three concurrent agents and remove the default limit of one `executor_sol` worker.
2. Change `executor_luna` and `tester` reasoning effort from `"xhigh"` to `"max"`.
3. Increase the default subagent report limits beyond 150 words for events and 250 words for final reports.
4. Allow more than two evidence-free retries before replacing a stuck or blocked worker.

Explain that stronger settings may increase token usage.

Ask the user to select individual options. Do not enable every option from a general “yes.”

If the user declines, keep the default configuration.

Apply selected changes as follows:

* **Option 1:** update `## Delegation` in `agent_docs/workflows/heavy_route.md`.
* **Option 2:** update `model_reasoning_effort` in:

  * `~/.codex/agents/executor_luna.toml`
  * `~/.codex/agents/tester.toml`
* **Option 3:** update the Event and Final report limits in the relevant agent `.toml` files.
* **Option 4:** update `## Thread Lifecycle and Waiting` in `agent_docs/workflows/heavy_route.md`.

After applying the selected changes, verify and report the final values.

## 3. Finish the installation

Report that the workflow installation is complete and instruct the user to restart Codex so the custom agent definitions are reloaded.

Do not automatically delete the downloaded `codex_workflows` directory.

Ask whether the user wants it removed. Delete it only if the user confirms.

