# Workflow Update

Supported command forms:

    codex_workflow --update

Python 3.11 or newer is required. The lifecycle CLI is dry-run by default.

## Source

The script queries GitHub Releases, selects the highest
non-draft SemVer release containing both the universal ZIP and `SHA256SUMS`,
verifies the checksum, and extracts it safely. It includes prereleases and
never clones the repository. The installed launcher delegates planning and
application to the verified incoming CLI so new migrations ship with the new
release.

## Plan and apply

Run:

```text
python3 ~/.codex/codex_workflow/workflow.py update --project <project> --json
```

For migration from a pre-script installation, run the incoming package's
`workflow.py` instead of an older installed launcher.

The script preserves valid configuration, project documents, personalization,
project-local instructions, unrelated workers/settings, source backups, and the
enabled/disabled state. It creates a verified timestamped backup and applies
the staged user/project state as one compensating transaction.

If a legacy project entry point contains merged local edits, the dry-run stops.
Review and extract only the project-local instructions into a temporary file,
then rerun with:

```text
--legacy-local-instructions <reviewed-file>
```

This is a one-time migration into the dedicated local region. Never infer the
content automatically.

Present the dry-run summary and request one confirmation. On confirmation,
rerun the identical command with `--apply --json`. A downgrade additionally
requires explicit approval and `--allow-downgrade`.

Report the installed version, preserved state, backup location, and any failure.
Do not describe a partial or rolled-back update as successful.
