# Workflow Setup Guide

Set up the custom Codex workflow for the current project. Do not inspect or modify project source-code files during this task.

The installation files are located in the downloaded `codex_workflows` directory. Read all `.md` and `.toml` files in that directory before starting.

Typical locations:

* Ubuntu and macOS: `codex_workflows/`
* Windows PowerShell: `codex_workflows\`

If the directory has another name or location, use its actual path.

## Path conventions

Resolve all project-relative paths from the root of the current project.

Examples:

* Ubuntu and macOS: `agent_docs/workflows/heavy_route.md`
* Windows: `agent_docs\workflows\heavy_route.md`

## 1. Install the default workflow

### 1.1 Install the main-agent instructions

Copy `AGENTS.md` from the installation directory to the root of the current project.

If the project already contains an `AGENTS.md` file, do not overwrite it automatically. Ask the user whether to:

* replace it;
* merge the workflow instructions into it;
* or cancel that part of the installation.

### 1.2 Create the project documentation structure

Create these directories if they do not already exist:

```text
agent_docs/
agent_docs/workflows/
```

Initialize the project documents required by `AGENTS.md` under `agent_docs/`.

Do not overwrite existing project documents without explicit user approval.

### 1.3 Install the workflow routes

Copy:

```text
heavy_route.md  → agent_docs/workflows/heavy_route.md
medium_route.md → agent_docs/workflows/medium_route.md
```

If either destination file already exists, ask the user before replacing it.

### 1.4 Install the custom subagents

Create the Codex user-agent directory if it does not already exist:

* Ubuntu and macOS: `~/.codex/agents/`
* Windows PowerShell: `$HOME\.codex\agents\`

Copy the following files into that directory:

```text
doc-writer.toml
tester.toml
executor_luna.toml
executor_sol.toml
```

Do not overwrite an existing agent definition without explicit user approval.

### 1.5 Verify the installation

Verify that:

* `AGENTS.md` exists in the project root;
* the required project documents exist under `agent_docs/`;
* `heavy_route.md` and `medium_route.md` exist under `agent_docs/workflows/`;
* all four agent definitions exist under the Codex user-agent directory;
* no unrelated project source files were modified.

Report the installed files, skipped files, conflicts, and any unresolved issues.

## 2. Configure the project

Ask the following questions one at a time.

### Core design principles

Ask:

> Would you like to define the work style and core design principles for this project?

Explain that this step is optional and provide a few relevant examples.

When the user provides instructions, add them under `## Core Design Principles` in the project-level `AGENTS.md`.

Do not remove existing project-specific instructions.

### Power profile

Explain that the default Heavy route is configured to conserve ChatGPT Plus usage.

Ask whether the user wants to enable any of these options:

1. Allow more than three concurrent agents and remove the default limit of one `executor_sol` worker.
2. Change `executor_luna` and `tester` reasoning effort from `"xhigh"` to `"max"`.
3. Increase the default subagent report limits beyond 150 words for events and 250 words for final reports.
4. Allow more than two evidence-free retries before replacing a stuck or blocked worker.

Explain that stronger settings may consume more tokens. Ask the user to select individual options; do not enable every option based only on a general confirmation.

If the user declines, keep the default configuration.

Apply selected changes as follows:

* **Option 1:** update `## Delegation` in `agent_docs/workflows/heavy_route.md`.
* **Option 2:** update `model_reasoning_effort` in:

  * `~/.codex/agents/executor_luna.toml`
  * `~/.codex/agents/tester.toml`
* **Option 3:** update the Event and Final report limits in the relevant agent TOML files.
* **Option 4:** update `## Thread Lifecycle and Waiting` in `agent_docs/workflows/heavy_route.md`.

Use the equivalent `$HOME\.codex\agents\` paths on Windows.

After applying the changes, verify and report the final values.

## 3. Finish the installation

Report that the workflow installation is complete and instruct the user to restart Codex so the custom agent definitions are reloaded.

Do not automatically delete the downloaded `codex_workflows` directory.

Ask whether the user wants it removed. Delete it only if the user confirms.

