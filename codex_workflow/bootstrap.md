# Initial Workflow Bootstrap

Use this guide only for the first installation from a universal GitHub Release
ZIP. Python 3.10 or newer is required. On Windows, use the equivalent
`py -3.10` invocation and native paths.

Verify `codex_workflow-<version>.zip` against `SHA256SUMS`, extract it into a
temporary directory, and require exactly one top-level `codex_workflow/`
directory. Validate the package first:

```text
python3 codex_workflow/workflow.py validate --package-root codex_workflow --json
```

Stop on any validation error. From the project being bootstrapped, run:

```text
python3 <extracted>/codex_workflow/workflow.py bootstrap \
  --package-root <extracted>/codex_workflow \
  --project <project>
```

The bootstrap installs the shared runtime, templates, source backup, user
command block, package-default configuration, distributed worker TOMLs, and
workflow-owned Codex settings. It also initializes the current project's
workflow entry point, documentation scaffold, personalization and state files,
and other project-level assets in one compensating transaction.

Restart Codex after the bootstrap succeeds.
