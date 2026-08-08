# Lifecycle Runtime Architecture

The lifecycle runtime separates immutable release inputs, mutable installed
state, generated outputs, and project-owned content.

## Data ownership

- `codex_workflow/resources/`: immutable defaults distributed by a release.
- `~/.codex/codex_workflow/workflow_config.json`: mutable installed state.
- Heavy snapshots, the End-of-Session fork value, active worker TOMLs, and
  workflow-owned Codex settings: generated outputs; never sources of truth.
- Project personalization: structured project state materialized into its own
  marker region.
- Project-local instructions: opaque preserved content in a separate marker
  region.

## Module boundaries

- `layout.py`: package and target path contracts.
- `config.py`: configuration schema and rendering.
- `migrations.py`: ordered persistent-resource migrations.
- `markers.py`: strict text-region parsing and rendering.
- `project_ops.py`: project entry point, personalization, and documents.
- `runtime_ops.py`: user-level runtime and generated outputs.
- `backup.py`: persistent update backups.
- `transaction.py`: atomic file writes and compensating rollback.
- `plan.py`: dry-run plans and compact summaries.
- `lifecycle.py`: composition only; it owns no low-level transformation.
- `release.py`: release selection, checksum, and safe extraction.
- `workflow.py`: CLI parsing, confirmation boundary, and incoming-runtime
  delegation.

## Upgrade contract

1. The installed launcher selects and verifies the incoming release.
2. The verified incoming CLI prepares and applies the update, so migrations
   ship with the target version.
3. Persistent resources pass through explicit schema migrations.
4. Generated surfaces are rendered from incoming templates and preserved
   persistent state.
5. Project-local regions and unrelated user files are preserved as opaque data.
6. Marker drift, missing migrations, or ambiguous legacy content stops before
   live writes.
7. Every write command is dry-run by default and uses one validated mutation
   plan for apply and rollback.

Add a new migration without changing callers: register the transformation from
schema `N` to `N+1`, add fixtures for both versions, and keep the incoming
default at the new schema.
