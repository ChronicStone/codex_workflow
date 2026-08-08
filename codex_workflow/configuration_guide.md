# Configure the Workflow

Run this procedure only when the user's trimmed message is exactly:

    codex_workflow --configure

The lifecycle CLI is:

    ~/.codex/codex_workflow/workflow.py

It requires Python 3.11 or newer and applies the validated configuration
directly.

## Questions

Read the current values from
`~/.codex/codex_workflow/workflow_config.json`. Show the current value with
every question and allow **Keep current**. Ask, in order:

The installed file is mutable state. Package defaults and migration fallbacks
come from `~/.codex/codex_workflow/resources/workflow_config.default.json` and
must not be edited as user configuration.

1. Default executor: `executor_luna` or `executor_terra`.
2. Default-executor reasoning effort: `high`, `xhigh`, or `max`.
3. Maximum concurrent workers, from 1 through the current platform limit of 20.
4. Maximum concurrent `executor_sol` instances.
5. Maximum worker final-report size in words.
6. End-of-Session context turns: a positive integer; default `200`.
The automatic session-start update check is controlled explicitly by
`codex_workflow --enable_auto_update` and
`codex_workflow --disable_auto_update`; do not change it in this questionnaire.

Ask only the follow-up needed for a valid value. Do not edit any live file
directly.

## Plan and apply

Run `python3 ~/.codex/codex_workflow/workflow.py configure` with only the
changed flags:

```text
--default-executor <name>
--reasoning-effort <effort>
--max-workers <count>
--max-sol <count>
--report-size <words>
--handoff-context-turns <count>
```

Run it with `--json` after collecting the requested values. The command
validates and applies the complete configuration in one operation.

The script validates the configuration, keeps `doc-writer` and
`end_of_session` enabled as required system roles, renders the Heavy snapshot
and handoff contract, installs the enabled worker TOMLs, removes only
manifest-owned disabled workers, and patches only workflow-owned Codex settings.
Report its result and tell the user to restart Codex when worker definitions or
platform settings changed.
