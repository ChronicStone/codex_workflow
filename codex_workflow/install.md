# Workflow Installation

Use the lifecycle CLI for both first bootstrap and installation into another
project. Do not manually copy or merge workflow files.

Python 3.11 or newer is required. On Windows, use the equivalent `py -3`
invocation and native paths.

## Release package

Install from the universal GitHub Release ZIP
`codex_workflow-<version>.zip`, not a repository checkout or source archive.
Verify it against `SHA256SUMS` and extract it into a temporary directory. The
archive must contain exactly one top-level `codex_workflow/` directory.

From the extracted package, validate it:

```text
python3 codex_workflow/workflow.py validate --package-root codex_workflow --json
```

Stop on any validation error.

## First bootstrap

From the project being installed, create a dry-run plan:

```text
python3 <extracted>/codex_workflow/workflow.py install \
  --package-root <extracted>/codex_workflow \
  --project <project> --json
```

Report the mutation summary and warnings, then request one confirmation. On
confirmation, rerun the identical command with `--apply --json`.

The script:

- installs the shared runtime, templates, source backup, user command block,
  active worker TOMLs, and workflow-owned Codex settings;
- preserves a valid existing workflow configuration and adds supported missing
  defaults;
- creates the project entry point and missing project documents;
- imports an existing unrecognized project `AGENTS.md` verbatim into the
  project-local marker region;
- creates the default personalization resource and project/user state
  manifests;
- stages and validates all outputs before applying a compensating transaction.

An existing `AGENTS.md` containing reserved workflow markers is a conflict and
must not be rewritten automatically.

## Install another project

Use the installed CLI:

```text
python3 ~/.codex/codex_workflow/workflow.py install \
  --project <project> --json
```

Confirm the dry-run, then rerun with `--apply --json`. This command changes only
the current project.

## Agent completion action

If the result contains a `doc-writer` action, initialize only the listed newly
created files. Preserve existing project documents. An empty project is valid;
record only verified context and leave deployment status empty when no active
plan exists.

Installation is incomplete until every reported agent action succeeds. Restart
Codex after a successful first bootstrap.
