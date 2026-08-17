# Initial Workflow Bootstrap

Use this guide only for the first installation from a universal GitHub Release
ZIP. Python 3.11 or newer is required. On Windows, use the equivalent
`py -3.11` invocation and native paths.

Verify `codex_workflow-<version>.zip` against `SHA256SUMS`, extract it into a
temporary directory, and require exactly one top-level `codex_workflow/`
directory. Validate the package first:

```text
python3 codex_workflow/workflow.py validate \
  --package-root codex_workflow --json
```

Stop on any validation error. From the project being bootstrapped, run:

```text
python3 <extracted>/codex_workflow/workflow.py bootstrap \
  --package-root <extracted>/codex_workflow \
  --project <project> --json
```

The bootstrap installs the shared runtime, role templates, source backup, user
command block, default configuration, worker TOMLs, and workflow-owned native
Codex agent settings. It also creates the current project's managed delegation
entry point, personalization resource, and lifecycle state in one compensating
transaction. Existing project instructions are preserved verbatim in the
project-local region.

The workflow deliberately creates no documentation scaffold and runs no worker
during installation. Verify that the result reports no agent actions, then
restart Codex so the new role definitions and configuration are loaded.

The recommended coordinator remains a user-owned top-level setting:

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
```

If those keys are absent, recommend adding them. Do not overwrite an existing
explicit coordinator model without the user's approval.
