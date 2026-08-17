# Workflow Installation

Use this procedure only to install the already-bootstrapped workflow into the
current project. Do not modify or reinstall user-level files.

Run:

```text
python3 ~/.codex/codex_workflow/workflow.py install \
  --project <project> --json
```

The command validates existing active or disabled workflow entry points. For a
new project it creates the managed delegation `AGENTS.md`, hidden
personalization and state files, and scoped `.gitignore` entries. An existing
unrecognized `AGENTS.md` is preserved verbatim inside the project-local region.

A valid active installation reports `already enabled`. A valid disabled entry
reports `already disabled`; use `codex_workflow --enable` to restore it. Stop on
stale, malformed, conflicted, or personalization-drifted state and report the
CLI's recovery instruction.

Project installation creates no documentation scaffold and calls no worker.
