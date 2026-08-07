# Check for Workflow Updates

Use this procedure only when the user's exact command is
`codex_workflow --check-update`. It is read-only: do not write installed
files, project files, temporary operational state, or Git metadata.

## Installed version

Read the authoritative installed version from:

```text
~/.codex/codex_workflow/VERSION
```

On Windows, resolve `~` through the current user's profile directory. Require
one valid SemVer value. The version marker in `~/.codex/AGENTS.md` is only
synchronized metadata and must not be used as the primary version source.

If the file is missing or invalid, report that the installed version is
invalid and recommend the initial release installation. Do not repair it from
this read-only command.

## Latest appropriate release

Query the GitHub Releases API:

```text
https://api.github.com/repos/viettran-edgeAI/codex_workflow/releases?per_page=100
```

Do not clone the repository, read a branch file, or use only
`/releases/latest`; the latter omits prereleases. Filter out drafts, ignore
releases whose tags are not valid SemVer after an optional leading `v`, and
ignore releases without the universal asset
`codex_workflow-<version>.zip`.

Choose the highest remaining semantic version, including prereleases. Require
the selected asset's `SHA256SUMS` entry when it is published. If no
appropriate release is available, report the API or release inconsistency and
make no changes.

## Compare and report

Compare the installed version with the selected release version using SemVer
ordering, including prerelease precedence. Report exactly one of:

- **current** — versions are equal;
- **update available** — the release is newer, with the release version and
  ZIP asset name;
- **installed version invalid** — the local `VERSION` is absent or invalid;
- **release unavailable or inconsistent** — no usable release asset could be
  selected.

If the installed version is newer than the highest release, report that no
update is available and do not downgrade it. `codex_workflow --update` is the
command that downloads and installs a selected release asset.

Remove only any temporary response or metadata used for the read-only check.
