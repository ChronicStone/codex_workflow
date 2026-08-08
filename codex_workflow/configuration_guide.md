# Configure the Workflow

Run the interactive procedure in this guide only when the user's trimmed
message is exactly:

    codex_workflow --configure

The persistent user-level resource is:

    ~/.codex/codex_workflow/workflow_config.json

The command may run from any directory after the user-level workflow is
installed. It does not change project personalization or project documents.

## Validate

Read the current JSON and worker templates from
`~/.codex/codex_workflow/templates/agents/` before asking questions. Stop if
the resource is missing, invalid, or uses an unsupported schema.

Rules:

- `default_executor` must be either `executor_luna` or `executor_terra`, and
  must be present in `enabled_workers`;
- `default_executor_reasoning_effort` must be one of `high`, `xhigh`, or
  `max`;
- `enabled_workers` contains unique workflow worker-template names and must
  include `doc-writer`, which project installation requires. Exactly one of
  `executor_luna` and `executor_terra` is enabled as the default executor;
- `max_concurrent_workers` is positive and does not exceed the platform limit;
- `max_executor_sol_instances` is between zero and
  `max_concurrent_workers`;
- `report_package_size` is a positive final-report word limit;
- all other enabled workers are preserved when the default executor changes.

## Questions

Show the current value with every question and allow **Keep current / skip / next**.
Treat each of these responses as retaining the current value and
advancing to the next question. Ask in this order:

1. Which default executor should be used? Choose `executor_luna` or
   `executor_terra`.
2. What reasoning effort should the default executor use? Choose `high`,
   `xhigh`, or `max`.
3. What is the maximum number of concurrent workers?
4. What is the maximum number of concurrent `executor_sol` instances?
5. What is the maximum worker final-report package size in words?

Ask only the minimum follow-up needed to make an answer valid. Present the
complete proposed JSON and request one confirmation before writing. If the
user cancels, change nothing.

## Apply

After confirmation:

1. Write and validate `workflow_config.json`.
2. Replace the block between `codex-workflow-effective-config-start/end` in
   `~/.codex/codex_workflow/heavy_route.md` with the final snapshot.
3. From `~/.codex/codex_workflow/templates/agents/`, install in
   `~/.codex/agents/` exactly the workflow TOMLs named by `enabled_workers`.
   Replace the other default-executor TOML when the selected default changes,
   and set the selected default executor's `model_reasoning_effort` to the
   confirmed `default_executor_reasoning_effort`. Back up and remove
   workflow-owned TOMLs that became disabled. Preserve unrelated TOMLs.
4. Update only workflow-owned keys in `~/.codex/config.toml`. Set
   `max_concurrent_threads_per_session` to the same integer as the confirmed
   `max_concurrent_workers` value written to `workflow_config.json`; do not
   leave the package default here when the user selected another value:

       [agents]
       enabled = true

       [features.multi_agent_v2]
       enabled = true
       max_concurrent_threads_per_session = <confirmed max_concurrent_workers>
       hide_spawn_agent_metadata = false
       tool_namespace = "agents"
       min_wait_timeout_ms = 300_000
       default_wait_timeout_ms = 300_000
       max_wait_timeout_ms = 3_600_000

   For example, if the confirmed workflow value is
   `"max_concurrent_workers": 3`, write
   `max_concurrent_threads_per_session = 3`.

The effective worker limit must not exceed the platform limit. Do not write
configuration into user/project `AGENTS.md`, `medium_route.md`, or worker role
content.

## Verify

- the JSON is valid;
- the Heavy route snapshot matches it;
- active workflow TOMLs match `enabled_workers` and include `doc-writer`;
- the default executor has an active TOML;
- the default executor's active TOML uses the selected reasoning effort;
- unrelated files and settings are unchanged.

Report the old and new effective values. Tell the user to restart Codex when
worker definitions or platform settings changed.

## Non-interactive lifecycle use

Installation copies the package default when the resource is missing and
applies it without asking configuration questions. Update preserves valid
values, adds new defaults, migrates supported schemas, and reapplies the final
snapshot without asking questions. Only `codex_workflow --configure` performs
interactive configuration.
