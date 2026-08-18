# Workflow Update

Supported command forms:

    codex_workflow --update

Python 3.11 or newer is required. The lifecycle CLI applies a validated update
directly.

## Source

The script queries GitHub Releases, selects the highest
non-draft SemVer release containing both the universal ZIP and `SHA256SUMS`,
verifies the checksum, and extracts it safely. It includes prereleases and
never clones the repository. The installed launcher delegates planning and
application to the verified incoming CLI so new migrations ship with the new
release.

## Update

Run:

```text
python3 ~/.codex/codex_workflow/workflow.py update
```

For migration from a pre-script installation, run the incoming package's
`workflow.py` instead of an older installed launcher.

The script migrates and preserves the mutable workflow configuration, then
regenerates distributed worker TOMLs from the incoming package templates. It
preserves unrelated Codex settings, source backups, and the automatic-check
preference. It creates a verified timestamped backup and applies the global
state as one compensating transaction.

Only installations that still have a workflow-owned project entry point should
also pass `--project <project>`. That path preserves project documents,
personalization, local instructions, and enabled/disabled state, and validates
the managed region against its recorded source version. Ordinary repository
`AGENTS.md` files are inherited alongside the global workflow and must not be
passed to the updater. When an older installed launcher automatically forwards
an ordinary project during delegation, the verified incoming updater ignores
that project and reports a warning while completing the global update.

If a legacy project entry point contains merged local edits, the update stops.
Review and extract only the project-local instructions into a temporary file,
then rerun with:

```text
--legacy-local-instructions <reviewed-file>
```

This is a one-time migration into the dedicated local region. Never infer the
content automatically. A downgrade additionally requires `--allow-downgrade`.

Report the installed version, preserved state, backup location, and any failure.
Do not describe a partial or rolled-back update as successful.
