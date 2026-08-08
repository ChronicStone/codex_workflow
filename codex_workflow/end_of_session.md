# End-of-Session Handoff

Use this handoff only when the user directly commands the exact phrase
`end this session`, ignoring capitalization and surrounding punctuation. It is
shared by Medium and Heavy routes.

Spawn one fresh worker with:

- `agent_type="end_of_session"`
- `task_name="end_of_session_handoff"`
<!-- codex-workflow-handoff-config-start -->
- `fork_turns="200"`
<!-- codex-workflow-handoff-config-end -->

Tell it the active route and pass through any extra handoff details from the
user. Do not summarize the session or build a task capsule. The finite fork
passes the configured number of recent turns so the worker can use its own Luna
xhigh model; its TOML contains the full procedure.

The worker owns the entire handoff, including status reconciliation,
documentation updates, compact closing checks, Git staging and commit, and the
final handoff report. The main agent must not duplicate those steps. Wait for
the worker, then relay its result to the user.

If the worker cannot be created or is blocked, report that limitation. Do not
silently transfer the handoff to Explorer or another role.
