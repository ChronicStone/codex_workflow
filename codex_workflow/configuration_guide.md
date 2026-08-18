# Configure the Workflow

Run this procedure only when the user's trimmed message is exactly:

    codex_workflow --configure

Read the current values from
`~/.codex/codex_workflow/workflow_config.json`, then show one menu with the
current value beside each setting:

1. Luna implementation effort: `high` or `xhigh`; `implementer` and
   `ui-implementer` default to `xhigh` because they own production changes.
2. Luna support effort: `high` or `xhigh`; scouts, testers, reviewers, UI
   reviewers, and documentation workers default to `high` for bounded evidence.
3. Maximum concurrent workers: 1 through 8.
4. Maximum worker final-report size in words.
5. Exit.

Ask only for the selected setting, allow **Keep current**, and return to the
menu. Do not edit generated files directly. When the user exits, run the CLI
once with only changed flags:

```text
python3 ~/.codex/codex_workflow/workflow.py configure --json \
  --implementation-effort <effort> \
  --support-effort <effort> \
  --max-workers <count> \
  --report-size <words>
```

The legacy `--reasoning-effort` flag remains available to set both effort groups
to the same value, but it cannot be combined with the role-specific flags. The
cumulative task worker budget is owned by
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
