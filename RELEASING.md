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
CHANGELOG.md
```

Every archive contains exactly this top-level directory and nothing beside it:

```text
codex_workflow/
├── VERSION
├── user_AGENTS.md
├── AGENTS.md
├── bootstrap.md
├── check_update.md
├── configuration_guide.md
├── disable.md
├── enable.md
├── install.md
├── personalization_guide.md
├── update.md
├── remove.md
├── enable_auto_check_update.md
├── disable_auto_check_update.md
├── enable_auto_update.md              # legacy alias
├── disable_auto_update.md             # legacy alias
├── workflow.py
├── runtime/
├── resources/                              # immutable package defaults
└── agents/
```

The package does not contain `README.md`, `illustration.png`,
`workflow_usage.md`, `RELEASING.md`, `CHANGELOG.md`, `.github/`, `scripts/`, `.git/`, or any
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
`VERSION=2.3.1` and tag `v2.3.1`. GitHub's prerelease flag is independent of
the SemVer string.

Add the release entry to `CHANGELOG.md` before tagging. The changelog is the
durable human-edited history; GitHub Releases may additionally include generated
commit notes.

## Local build and validation

Run these commands from the repository root. The builder uses only Python's
standard library, requires Python 3.11 or newer, and works on Linux, macOS, and
Windows.

Linux/macOS:

```sh
version="$(cat codex_workflow/VERSION)"
tag="v$version"
python3 -B scripts/test_workflow_runtime.py -v
python3 scripts/package_release.py --release-tag "$tag" --output-dir dist
python3 scripts/package_release.py --verify dist/codex_workflow-*.zip
```

Windows PowerShell:

```powershell
$version = (Get-Content codex_workflow\VERSION).Trim()
$tag = "v$version"
py -3.11 -B scripts\test_workflow_runtime.py -v
py -3.11 scripts\package_release.py --release-tag $tag --output-dir dist
py -3.11 scripts\package_release.py --verify "dist\codex_workflow-$version.zip"
```

The build validates the version, marker, lifecycle runtime, and required
resources; rejects generated Python caches; creates a deterministic ZIP asset;
and writes `dist/SHA256SUMS`. Run the runtime tests before packaging and inspect
the archive listing when package contents change.

## Publishing — approval required

Do not run the following commands until the release structure, contents, tag,
and prerelease setting have been approved:

```sh
git status --short
version="$(cat codex_workflow/VERSION)"
tag="v$version"
git tag -a "$tag" -m "codex_workflow $tag"
git push origin "$tag"
```

Pushing a semantic `v*` tag starts `.github/workflows/release.yml`. It rebuilds
and validates the archives from that tagged commit, then publishes a stable
GitHub Release with generated notes. Manual dispatch packages the selected
workflow ref, rejects an existing release tag that points elsewhere, and
defaults to prerelease publication.

If the workflow is unavailable, the equivalent manual publication command is:

```sh
gh release create "$tag" \
  "dist/codex_workflow-$version.zip" \
  dist/SHA256SUMS \
  --title "codex_workflow $tag" \
  --generate-notes
```

The manual command is also approval-gated and must use assets built from the
same tagged commit.

## Consumer commands

- Initial installation reads the extracted release package's
  `codex_workflow/bootstrap.md`; the bundled lifecycle CLI validates and
  applies the user-level bootstrap transaction directly.
- `codex_workflow --install` reads the installed `install.md` and reports the
  globally enabled version; no per-project installation is required.
- At session start, the installed runtime checks GitHub Releases once when
  `auto_check_update` is enabled and reports an available update.
- `codex_workflow --enable_auto_check_update` explicitly enables that check in
  mutable installed configuration.
- `codex_workflow --disable_auto_check_update` disables it again. The former
  `--enable_auto_update` and `--disable_auto_update` prompts remain compatibility
  aliases; no command automatically installs an update.
- `codex_workflow --update` selects the latest appropriate ZIP asset, downloads
  it from its GitHub Release URL, verifies it, and updates the global runtime.
  It never clones the repository or modifies an ordinary project `AGENTS.md`.
- `codex_workflow --remove` first displays a destructive dry-run summary and
  requires one explicit second confirmation before deleting workflow-owned
  files.
