# Personalize the Current Project

Run the interactive procedure in this guide only when the user's trimmed
message is exactly:

    codex_workflow --personal

The persistent project resource is:

    .codex_workflow_hidden_resource/personalization.md

The command changes only the current project. It does not change user-level
workflow configuration or project documents.

## Default resource

Installation creates this resource when missing:

```markdown
# Project Workflow Personalization

## Frontend Project Profile
Status: default
Decision: No additional frontend profile.

## Design Principles
Status: default
Decision: Preserve the default core design principles.

## Additional Workflow Decisions
Status: default
Decision: No additional project-scoped workflow decisions.
```

Each status is `default`, `customized`, or `skipped`. Store only confirmed
project-scoped decisions. Never store secrets, conversation logs, temporary
state, or user-level worker configuration.

## Validate

Select exactly one recognized entry point:

- `AGENTS.md` when enabled;
- `.codex_workflow_hidden_resource/.AGENTS.md` when disabled.

Stop if neither or both exist. Read and validate the current personalization
resource without writing it. If it is missing, use the default resource below
as an in-memory recovery candidate and report the recovery before continuing.
If it is invalid, preserve the invalid file, report the validation error, and
use the default resource only as an explicitly confirmed reset proposal. A
missing or invalid resource must remain unchanged when the user cancels.

## Questions

Show the current decision with every question and allow **Keep current** or
**Reset to default**. Ask in this order:

1. Frontend Project Profile: should this project apply a frontend-specific
   workflow profile, including reduced frontend verification?
2. Design Principles: which project design principles should Codex follow?
3. Additional Workflow Decisions: are there other project-scoped workflow
   instructions to apply?

Ask only the minimum follow-up needed to turn an answer into a direct
instruction. For a missing or invalid resource, do not offer **Keep current**
until a valid current value exists; present the default as a recovery/reset
proposal. Present the complete proposed personalization resource and request
one confirmation before writing. If the user cancels, change no file, including
the missing or invalid resource.

## Apply

After confirmation:

1. Build and validate the proposed resource and the materialized entry point in
   a temporary staging area. Replace only the content between
   `codex-workflow-project-personalization-start/end` with direct instructions
   derived from customized decisions.
2. Commit the staged resource and entry point together. Leave the marker body
   empty when every decision is default or skipped. Preserve the enabled/
   disabled path and all content outside the marker body.
3. If either replacement fails, restore the previous resource and entry point
   from their pre-change copies and verify the rollback. If the resource was
   previously missing, remove the newly created resource during rollback. If
   rollback fails, report the affected files as a recovery blocker.

Do not insert the resource path, guide name, a generated Design Principles
heading, or user-level configuration into the entry point.

## Verify

- exactly one recognized entry point still exists;
- the resource is valid and contains all three sections;
- the entry point contains direct instructions matching the final resource;
- project documents and user-level configuration are unchanged.

Report the decisions changed and those kept.

## Non-interactive lifecycle use

Project installation creates the default resource and materializes an empty
personalization marker without asking questions. Update preserves and
reapplies the current resource without asking questions. Only
`codex_workflow --personal` performs interactive personalization.
