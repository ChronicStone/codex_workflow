# Workflow Update

Use this procedure only when the user sends `codex_workflow --update`.

## Source and Identity

- Repository: `https://github.com/viettran-edgeAI/codex_workflow`
- Installed version: the `codex-workflow-version` marker in `~/.codex/AGENTS.md`
- Latest version: the `codex-workflow-version` marker in
  `codex_workflow/user_AGENTS.md` on the repository's default branch
- Project marker: `<!-- codex-workflow-id: viettran-edgeAI/codex_workflow -->`
- User-level marker: `<!-- codex-workflow-user-id: viettran-edgeAI/codex_workflow -->`

## Procedure

1. Confirm `~/.codex/AGENTS.md` contains the exact user-level marker. If not, stop
   and tell the user to run the initial README installation.
2. Read the installed user-level version. A missing or invalid value means a user-level
   repair update is required. Do not use the project `AGENTS.md` as the version
   source.
3. If the current project has the project marker, read
   `agent_docs/workflow_personalization.md` and the current `## Project Context`
   body before any replacement. A missing personalization record requires the
   migration fallback in `personalization.md`.
4. Retrieve the latest repository `README.md` and `user_AGENTS.md`.
5. Require the README marker and user-level AGENTS marker to contain the same
   version. Stop on a mismatch because the release is inconsistent.
6. Compare semantic versions:
   - equal: report that the workflow is current and stop;
   - installed is newer: do not downgrade without explicit user approval;
   - repository is newer, or the installed version is invalid: continue.
7. Execute the exact installation prompt under `## 1. Installation` in the
   latest README. That prompt reads the bundled `install.md`; do not create a
   separate update implementation.
8. Run the user-level installation phase to replace `~/.codex/codex_workflow/`,
   `~/.codex/agents/`, and the workflow-owned sections of `~/.codex/AGENTS.md`.
9. If the current project has the project marker, run the project update phase
   and let `personalization.md` reapply the complete record, including the
   generated `## Workflow Configuration` section and protected `## Project
   Context` content. If it does not, update only the user-level installation.
10. Verify the new version in `~/.codex/AGENTS.md`, report old and new versions,
    and instruct the user to restart Codex if user-level agent definitions changed.

Do not preserve other modifications to workflow-owned files unless the latest
`install.md` or `personalization.md` explicitly requires it.
