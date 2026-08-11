# Legacy Alias: Disable Automatic Update Checks

Use the canonical prompt `codex_workflow --disable_auto_update`. This guide is
kept so installations that still recognize the former
`codex_workflow --disable_auto_check_update` prompt remain compatible.

Run the lifecycle CLI directly:

```text
python3 ~/.codex/codex_workflow/workflow.py \
  disable-auto-update --json
```

Report the final `auto_check_update` value. The script sets the mutable installed
configuration and removes the session-start check instruction from the
workflow's managed region in `~/.codex/AGENTS.md`. It preserves unrelated user
content and does not rewrite routes, workers, project files, or package defaults.
