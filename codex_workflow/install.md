# Workflow Installation

Use this procedure only to verify an already-bootstrapped global installation.
The workflow is inherited automatically in every repository.

Run:

```text
python3 ~/.codex/codex_workflow/workflow.py install --json
```

The command reports `globally enabled` with the installed version. It does not
modify the current repository's `AGENTS.md`, `.gitignore`, or hidden files;
repository instructions layer naturally after the global workflow policy. It
calls no worker.
