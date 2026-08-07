# Enable the Project Workflow

## Operation

Target: the project's disabled workflow entry point.

Source:

    .codex_workflow_hidden_resource/.AGENTS.md

Target path:

    AGENTS.md

Enabling the workflow changes only the entry-point state. Do not reread or
reapply configuration or personalization resources during this operation; the
effective values were materialized in the entry point earlier.

Perform these actions:

1. Confirm that `.codex_workflow_hidden_resource/.AGENTS.md` has the exact
   project marker.
2. Refuse to continue if `AGENTS.md` already exists or both entry points exist.
3. Record a checksum of `.codex_workflow_hidden_resource/.AGENTS.md`.
4. Move the hidden entry point to `AGENTS.md` without editing its contents.
5. Confirm that the checksum is unchanged.
6. Verify that the project personalization resource, entry-point contents,
   project documents, workflow payload, and user-level workers remain intact.

If the project is already enabled with a recognized `AGENTS.md`, report a safe
no-op. An unmarked file is a conflict and must not be replaced.

The state transition is:

    .codex_workflow_hidden_resource/.AGENTS.md -> AGENTS.md

Do not delete the resource, project documents, runtime payload, workers, source
package, or backups.
