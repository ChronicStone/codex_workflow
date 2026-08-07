# Workflow Update

Supported command forms:

    codex_workflow --update
    codex_workflow --update --source <PACKAGE>

Both forms update the installed user-level workflow and the recognized current
project while preserving configuration, personalization, project documents,
local instructions, and enabled/disabled state.

Default source:

    https://github.com/viettran-edgeAI/codex_workflow/releases

With `--source`, resolve `<PACKAGE>` as one local extracted release-package
path. Accept either the `codex_workflow/` package root or its parent containing
exactly one `codex_workflow/` directory. Do not query or download a release in
this mode. Normalize and validate the source before changing installed state,
and keep it unchanged.

## Default release selection

Query the GitHub Releases API rather than cloning the repository:

```text
https://api.github.com/repos/viettran-edgeAI/codex_workflow/releases?per_page=100
```

Ignore drafts, require a valid semantic version in each tag, and choose the
highest semantic version that has the universal ZIP asset and a matching
`SHA256SUMS` entry. Include prereleases while this project is distributing
prereleases; the GitHub `/releases/latest` endpoint is not sufficient because
it omits prereleases. Do not use a branch file as the update source.

## 1. Select, validate, and preflight without live writes

Before changing any installed or project file, read the installed `VERSION`,
select the latest appropriate release using the rules above, and compare the two
values using SemVer ordering. If they are equal, report that the workflow is
current and stop. If the installed version is newer, do not downgrade it
without explicit approval.

For an available update, download the selected ZIP asset from its
`browser_download_url`, verify its checksum, and extract it into a temporary
directory. Require the extracted `codex_workflow/VERSION` and
`user_AGENTS.md` marker to match the release tag before continuing. Never clone
or pull the repository as an update source.

For `--source`, skip default release selection. Read the installed and incoming
`VERSION` values and compare them with SemVer ordering. Require explicit
approval before using an older local package. An equal-version local package
may continue as a repair/reapply update. Require its `user_AGENTS.md` marker to
match its `VERSION` before continuing.

Then validate, without replacing live files:

1. Validate incoming `VERSION`, markers, configuration schema, project entry
   template, all six project-document templates, routes, guides,
   `explorer_companion.md`, `end_of_session.md`, and worker TOMLs.
2. Validate the incoming user marker, installed `VERSION`, and
   `~/.codex/codex_workflow/workflow_config.json`.
3. Resolve the current project state before any user-level update is written:
   - update `AGENTS.md` when it has the project marker;
   - update `.codex_workflow_hidden_resource/.AGENTS.md` when it is the only
     recognized entry point, keeping the project disabled;
   - stop if both entry points exist;
   - if an unrecognized `AGENTS.md` exists, offer **Overwrite all** or
     **Merge**, and obtain the choice before preparing a replacement;
   - if no workflow entry point exists, mark the project as user-level-only and
     do not create one during this update.
4. For a recognized entry point, load and preserve
   `.codex_workflow_hidden_resource/personalization.md`. If it is missing, use
   the default resource from `personalization_guide.md` as an in-memory recovery
   candidate and report the recovery; do not write it yet.
5. Prepare the project candidate in a temporary directory. Three-way merge the
   old installed project template (base), current entry point (local), and
   incoming template (new), preserving project-local additions and the selected
   active or disabled path. Reapply the preserved personalization snapshot in
   the candidate. Resolve unambiguous changes automatically and ask the user
   only about actual merge conflicts.
6. Verify the candidate has exactly one entry point and that every existing
   file in `agent_docs/` is preserved. If a merge conflict, user choice,
   validation, or preflight check remains unresolved, stop now without changing
   any installed or project file.

If an old installed template is unavailable, prepare a conservative candidate
from the incoming template and local entry point; request input only for
passages whose ownership cannot be determined. Keep all candidate files in the
temporary staging area until the update is committed.

## 2. Stage the complete update

After preflight succeeds, create one temporary staging area and build the full
target state there. Do not copy incoming files directly over live files.

1. Stage the incoming `user_AGENTS.md`, lifecycle guides, configuration and
   personalization guides, routes, `explorer_companion.md`,
   `end_of_session.md`, and `VERSION` in a target-relative tree whose final
   destination is `~/.codex/codex_workflow/`.
2. Preserve the installed `workflow_config.json`; migrate its supported schema
   and merge missing fields from the incoming default. Validate the final
   snapshot and stage its synchronized Heavy route, active workflow TOMLs, and
   workflow-owned platform settings without asking configuration questions. If
   a value cannot be migrated safely, stop and report the migration blocker;
   configuration changes belong to `codex_workflow --configure`.
3. Extract the body between `codex-workflow-user-managed-start/end` in the
   incoming `user_AGENTS.md`. Stage the replacement for `~/.codex/AGENTS.md`,
   preserving every unrelated instruction.
4. Retain the old installed project template as the merge base, then stage the
   incoming project template, `agents/*.toml`, and `project_docs/*.md` under
   their target-relative template paths.
5. Stage the complete incoming package at the target-relative path
   `.source_backup/<new-version>/` and preserve older source backups.
6. Stage the project entry point and personalization recovery/candidate from
   the preflight. Never stage replacements for `agent_docs/`.

Do not write configuration or guide references into runtime entry points or
routes.

## 3. Commit or roll back the staged update

1. After the staged state passes its final validation, back up the installed
   workflow payload, project template, user `AGENTS.md`, workflow-owned worker
   TOMLs, and recognized project entry point with its personalization resource
   under `~/.codex/codex_workflow/.backups/<old-version>-<timestamp>/`.
2. Verify the backups before replacing anything. If backup creation or
   verification fails, stop with all live files unchanged.
3. Apply the staged user-level and recognized-project state as one lifecycle
   operation. Preserve the selected enabled/disabled path and do not create the
   other entry point. For a project with no workflow entry point, apply only the
   user-level state and report that the project remains uninstalled.
4. If any replacement fails, stop immediately, restore every target already
   replaced from the verified backups, and verify the rollback. Report the exact
   rollback result; never report a partial update as successful. If rollback
   itself fails, report the affected files as a recovery blocker. If a missing
   personalization resource was recovered in staging, rollback removes that
   newly created resource because no previous file existed to restore.

## 4. Verify

- installed and incoming versions and markers are consistent;
- guides, configuration, project entry/documentation templates, routes,
  `explorer_companion.md`, `end_of_session.md`, and source backup exist under
  `~/.codex/codex_workflow/`;
- Heavy route and active workflow TOMLs match the preserved configuration;
- the project entry point includes the new workflow template changes and the
  preserved project-local changes;
- personalization is unchanged unless explicitly edited and is materialized
  in the selected entry point;
- all existing project documents, unrelated workers, unrelated Codex settings,
  activation state, source packages, and backups are preserved;
- rerunning update produces the same valid state or reports a specific merge
  conflict.
