# Disable the Project Workflow

## Operation

Target: the project's active workflow entry point.

Source:

    AGENTS.md

Target path:

    .codex_workflow_hidden_resource/.AGENTS.md

Perform these actions:

1. Confirm that `AGENTS.md` has the exact project marker.
2. Refuse to continue if `.codex_workflow_hidden_resource/.AGENTS.md` already
   exists or both entry points exist.
3. Record a checksum of `AGENTS.md`.
4. Create `.codex_workflow_hidden_resource/` when needed, then move
   `AGENTS.md` to `.codex_workflow_hidden_resource/.AGENTS.md` without editing
   its contents.
5. Confirm that the checksum is unchanged.
6. Verify that the project personalization resource, entry-point contents,
   project documents, workflow payload, and user-level workers remain intact.

If the project is already disabled with a recognized hidden entry point,
report a safe no-op. An unmarked file is a conflict and must not be replaced.

The state transition is:

    AGENTS.md -> .codex_workflow_hidden_resource/.AGENTS.md

Do not delete the resource, project documents, runtime payload, workers, source
package, or backups.
