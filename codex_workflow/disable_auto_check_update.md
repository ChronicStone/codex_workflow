# Disable Automatic Update Checks

Run this procedure only for the exact command:

    codex_workflow --disable_auto_check_update

The command itself is explicit authorization to disable the session-start
check; do not request another confirmation.

Run a dry-run first:

```text
python3 ~/.codex/codex_workflow/workflow.py \
  disable-auto-check-update --json
```

If the plan is valid, immediately rerun it with `--apply --json`. Report the
final `auto_check_update` value. The script changes only the mutable installed
`workflow_config.json`; it does not rewrite routes, workers, project files, or
package defaults.

The setting can be enabled again through `codex_workflow --configure`.
