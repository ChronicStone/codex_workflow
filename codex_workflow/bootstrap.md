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

## Required documentation action

Read the command's `agent_actions` result. It always contains one required
`doc-writer` action for the Project Documentation Framework. Spawn it with
`agent_type="doc-writer"`, `task_name="bootstrap_docs"`, and
`fork_turns="none"`. Its capsule must include the project root and the returned
`files`, `framework`, and `required_context_files` lists, with these
requirements:

- Inspect only enough project evidence to record verified initial context;
  source-less projects are valid.
- Initialize only documents listed in `files` and remove their
  `codex-workflow-bootstrap-template` markers.
- Populate newly created `project_structure.md`, `project_overview.md`, and
  `project_core_tech.md` with verified project structure, purpose/architecture,
  and technology context. If relevant source is absent, explicitly record that
  fact instead of leaving template-only content.
- Preserve every pre-existing project document. If `files` is empty, perform a
  read-only completeness check of all documents in `framework`.
- This action may initialize newly created `project_progress.md` and
  `latest_session_work.md`; leave deployment status empty when no plan exists.
- Do not edit source, entry points, personalization, Git state, or user-level
  files.

Verify that every framework file exists, no newly created file retains the
bootstrap marker, and every newly created file in `required_context_files` has
been populated. Installation is incomplete if the required worker cannot run or
fails; do not silently perform its work in the main thread.

Restart Codex only after the bootstrap and required documentation action both
succeed.
