# Personalize the Current Project

Run this procedure only when the user's trimmed message is exactly:

    codex_workflow --personal

The persistent resource is:

    .codex_workflow_hidden_resource/personalization.md

The lifecycle CLI is dry-run by default and requires Python 3.11 or newer:

    ~/.codex/codex_workflow/workflow.py

## Questions

Read the current resource. Ask, in order:

1. Frontend Project Profile.
2. Design Principles.
3. Additional Workflow Decisions.

Show the current decision and allow **Keep current** or **Reset to default**.
Store only confirmed project-scoped instructions. Never store secrets, logs,
temporary state, or worker configuration.

## Plan and apply

Write the complete proposed resource to a temporary file. Run:

```text
python3 ~/.codex/codex_workflow/workflow.py personalize \
  --project <project> --resource <candidate> --json
```

Present the proposed decisions and mutation summary, then request one
confirmation. On confirmation, rerun with `--apply --json`. Delete the temporary
candidate afterward. Cancellation changes no live file.

The script validates all three sections and atomically updates the resource and
the generated personalization region. It preserves the workflow-managed and
project-local regions and the enabled/disabled entry-point state.
