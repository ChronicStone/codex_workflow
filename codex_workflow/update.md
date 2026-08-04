# Workflow Update

Use this procedure only when the user sends `codex_workflow --update`.

## Source and Identity

- Repository: `https://github.com/viettran-edgeAI/codex_workflow`
- Installed version: the plain-text value in `~/.codex/codex_workflow/VERSION`
- Latest version: the semantic version in the latest GitHub Release tag
- Release package version: the plain-text value in
  `codex_workflow/VERSION` inside the downloaded release package
- Compatibility marker: the `codex-workflow-version` marker in
  `codex_workflow/user_AGENTS.md`
- Project marker: `<!-- codex-workflow-id: viettran-edgeAI/codex_workflow -->`
- User-level marker: `<!-- codex-workflow-user-id: viettran-edgeAI/codex_workflow -->`

## Procedure

1. Confirm `~/.codex/AGENTS.md` contains the exact user-level marker. If not, stop
   and tell the user to run the initial release installation.
2. Read `~/.codex/codex_workflow/VERSION`. A missing or invalid value means a
   user-level repair update is required. Do not use the project `AGENTS.md` or
   the marker in `~/.codex/AGENTS.md` as the primary version source.
3. If the current project has the project marker, read
   `agent_docs/workflow_personalization.md` and the current `## Project Context`
   body before any replacement. A missing personalization record requires the
   migration fallback in `personalization.md`.
4. Query the latest GitHub Release and read its semantic version tag. Normalize
   an optional leading `v` before comparing it with `VERSION`. Do not retrieve
   or read `README.md`.
5. Compare the installed version with the release tag:
   - equal: report that the workflow is current and stop;
   - installed is newer: do not downgrade without explicit user approval;
   - release is newer, or the installed version is invalid: continue.
6. Download and extract the release asset into a temporary directory. Read
   `codex_workflow/VERSION` from that package and require it to match the
   release tag. Also require the marker in `codex_workflow/user_AGENTS.md` to
   match `VERSION`. Stop on a mismatch because the release is inconsistent.
7. Read the package's `codex_workflow/install.md` for the user-level
   installation procedure. Do not read or execute instructions from
   `README.md`.
8. Run that user-level installation phase to replace `~/.codex/codex_workflow/`,
   `~/.codex/agents/`, and the workflow-owned sections of `~/.codex/AGENTS.md`.
9. If the current project has the project marker, run the project update phase
   and let `personalization.md` reapply the complete record, including the
   generated `## Workflow Configuration` section and protected `## Project
   Context` content. If it does not, update only the user-level installation.
10. Verify the new version in `~/.codex/codex_workflow/VERSION` and that the
    marker in `~/.codex/AGENTS.md` matches it. Report old and new versions, and
    instruct the user to restart Codex if user-level agent definitions changed.

Do not preserve other modifications to workflow-owned files unless the latest
`install.md` or `personalization.md` explicitly requires it.
