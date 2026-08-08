# Disable Automatic Update Checks

Run this procedure only for the exact command:

    codex_workflow --disable_auto_update

The command itself is explicit authorization to disable the session-start
check; do not request another confirmation.

Run the lifecycle CLI directly:

```text
python3 ~/.codex/codex_workflow/workflow.py \
  disable-auto-update --json
```

Report the final `auto_check_update` value. The script changes only the mutable
installed `workflow_config.json`; it does not rewrite routes, workers, project
files, or package defaults.

The setting is enabled again through `codex_workflow --enable_auto_update`.
