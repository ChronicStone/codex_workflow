# Workflow Personalization

This document defines how project-specific installation decisions are recorded
and reapplied. It is workflow procedure, not the project's answer record.

The project-owned record is:

```text
agent_docs/workflow_personalization.md
```

Never replace that file during installation or workflow update. It is the
source of truth for configuration decisions made for the current project.

## Record format

Create the record with this structure if it does not exist:

```markdown
# Workflow Personalization

## Workflow Style and Design Principles

Status: default | customized | skipped

Decision:

## Frontend Project Profile

Status: default | customized | skipped

Decision:

## Power Profile

- option_1_more_workers_and_executor_sol: disabled
- option_2_max_reasoning_for_luna_and_tester: disabled
- option_3_larger_worker_reports: disabled
- option_4_more_evidence_free_retries: disabled

## Additional Workflow Decisions

Decision:
```

Use the user's wording when it carries a project-specific constraint. Record
`default` or `skipped` explicitly; an omitted value is an unresolved decision.
Do not store secrets, credentials, or transient conversation logs.

## Initial installation

1. Read the existing project record if present.
2. Ask the configuration questions one at a time.
3. After each answer, write the answer to the project record before applying it.
4. If the user skips a question, record `skipped` and use the default.
5. Apply the complete record to the newly installed workflow.
6. Add or update `## Workflow Configuration` in the project `AGENTS.md` with a
   concise summary of effective choices.

Do not ask again for a decision already recorded in the project file unless the
user explicitly requests reconfiguration.

## Applying the record

Apply decisions to the owning files:

- Workflow style and design principles → `## Core Design Principles` in
  `AGENTS.md`.
- Frontend profile → the relevant testing, modularization, and design rules in
  `AGENTS.md`.
- Option 1 → delegation limits in
  `~/.codex/codex_workflow/heavy_route.md`.
- Option 2 → `model_reasoning_effort` in
  `~/.codex/agents/executor_luna.toml` and `tester.toml`.
- Option 3 → event/final report limits in the relevant agent TOML files and
  route instructions.
- Option 4 → retry rules in
  `~/.codex/codex_workflow/heavy_route.md`.
- Additional workflow decisions → the owning route, agent definition, or
  `AGENTS.md` section after confirming the requested scope.

Preserve the current `## Project Context` content from a recognized `AGENTS.md`
unless the project record explicitly provides a replacement. Preserve other
project-specific instructions outside workflow-owned sections unless the user
authorizes their replacement.

## Workflow update

Before the installer replaces a recognized `AGENTS.md` or user-level workflow:

1. Read `agent_docs/workflow_personalization.md`.
2. Keep its complete contents unchanged.
3. Replace the workflow-owned files.
4. Reapply every recorded decision to the new files.
5. Restore `## Project Context` and any project-specific content protected by
   the install procedure.
6. Regenerate `## Workflow Configuration` in the new `AGENTS.md`.

If the record is missing during an update, preserve the existing
`## Project Context` and `## Core Design Principles`, create the record, and ask
only the configuration questions whose decisions cannot be recovered safely.
Report this migration explicitly.

## Completion checks

Verify that:

- the project record exists and contains explicit values for every configuration
  question;
- `AGENTS.md` contains the effective `## Workflow Configuration` summary;
- route and agent settings match the recorded power profile;
- no project personalization file was overwritten or deleted.
