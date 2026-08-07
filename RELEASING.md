# Release Process

This repository publishes the workflow as GitHub Release assets. The release
payload is intentionally independent of the repository presentation and
development files.

## Repository and asset layout

The repository-only release machinery is:

```text
.github/workflows/release.yml
scripts/package_release.py
RELEASING.md
```

Every archive contains exactly this top-level directory and nothing beside it:

```text
codex_workflow/
├── VERSION
├── user_AGENTS.md
├── AGENTS.md
├── install.md
├── update.md
├── check_update.md
├── workflow_config.json
├── agents/
└── project_docs/
```

The package does not contain `README.md`, `illustration.png`,
`workflow_usage.md`, `RELEASING.md`, `.github/`, `scripts/`, `.git/`, or any
other repository-only file. All files below `codex_workflow/` are included so
the installed workflow remains self-contained.

Each GitHub Release publishes one universal asset for every supported operating
system:

- `codex_workflow-<version>.zip`;
- `SHA256SUMS` for the ZIP asset.

## Versioning

Use SemVer 2.0.0. Keep the plain version in `codex_workflow/VERSION` and the
`codex-workflow-version` marker in `codex_workflow/user_AGENTS.md` identical.
The release tag is the same value with an optional leading `v`, for example
`VERSION=1.1.0` and tag `v1.1.0`. GitHub's prerelease flag is independent of
the SemVer string; the initial releases are marked as prereleases by the
workflow.

## Local build and validation

Run these commands from the repository root. The builder uses only Python's
standard library and works on Linux, macOS, and Windows.

Linux/macOS:

```sh
python3 scripts/package_release.py --release-tag v1.1.0 --output-dir dist
python3 scripts/package_release.py --verify dist/codex_workflow-*.zip
```

Windows PowerShell:

```powershell
py -3 scripts/package_release.py --release-tag v1.1.0 --output-dir dist
py -3 scripts/package_release.py --verify dist\codex_workflow-1.1.0.zip
```

The build validates the version and marker, creates a deterministic ZIP asset,
validates it, and writes `dist/SHA256SUMS`. Inspect the archive listing before
publication if the package contents changed.

## Publishing — approval required

Do not run the following commands until the release structure, contents, tag,
and prerelease setting have been approved:

```sh
git status --short
git tag -a v1.1.0 -m "codex_workflow v1.1.0"
git push origin v1.1.0
```

Pushing a semantic `v*` tag starts `.github/workflows/release.yml`. It rebuilds
and validates the archives from that tagged commit, then publishes the GitHub
Release with `--prerelease` and generated notes. The workflow also supports a
manual dispatch with a tag and defaults to prerelease publication. The
prerelease flag should be removed or disabled only after a separate decision to
promote the project to stable releases.

If the workflow is unavailable, the equivalent manual publication command is:

```sh
gh release create v1.1.0 \
  dist/codex_workflow-1.1.0.zip \
  dist/SHA256SUMS \
  --title "codex_workflow v1.1.0" \
  --generate-notes \
  --prerelease
```

The manual command is also approval-gated and must use assets built from the
same tagged commit.

## Consumer commands

- `codex_workflow --install` reads the extracted release package's
  `codex_workflow/install.md` and installs the current project workflow. The
  initial user-level installation starts from a release asset.
- `codex_workflow --check-update` queries the Releases API, includes
  prereleases, compares SemVer values, and makes no changes.
- `codex_workflow --update` selects the latest appropriate ZIP asset, downloads
  it from its GitHub Release URL, verifies it, and follows the package's update
  procedure. It never clones the repository.
