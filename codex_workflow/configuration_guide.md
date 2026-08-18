# Configure the Workflow

Run this procedure only when the user's trimmed message is exactly:

    codex_workflow --configure

Read the current values from
`~/.codex/codex_workflow/workflow_config.json`, then show one menu with the
current value beside each setting:

1. Luna worker effort: `high` or `xhigh`; the default and all role templates use
   `xhigh` so bounded workers can complete substantive work without Sol rework.
2. Maximum concurrent workers: 1 through 8.
3. Maximum worker final-report size in words.
4. Exit.

Ask only for the selected setting, allow **Keep current**, and return to the
menu. Do not edit generated files directly. When the user exits, run the CLI
once with only changed flags:

```text
python3 ~/.codex/codex_workflow/workflow.py configure --json \
  --reasoning-effort <effort> \
  --max-workers <count> \
  --report-size <words>
```

The reasoning setting is an explicit override for the default Luna subagent and
general implementer. The cumulative task worker budget is owned by
`workflow_config.json`, defaults to six, and is separate from native
concurrency. The CLI validates and applies one configuration transaction,
updates native `[agents]` settings, materializes every owned role, and preserves
unrelated Codex config.

Agent identity is a policy-level naming convention, not a configuration option:
use `<role> — <task ID>` keyed by native `agent_id` in commentary, plans, worker
ledgers, and final reports. Native generated person nicknames cannot be
overridden and are mentioned only when quoting a native platform error.

Automatic update checks are controlled separately by
`codex_workflow --enable_auto_check_update` and
`codex_workflow --disable_auto_check_update`. Tell the user to restart Codex
after agent definitions or platform settings change.
