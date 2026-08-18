# Analyze a Workflow Thread

Run this procedure when the user's trimmed message matches:

    codex_workflow --analyze-thread <native-session-id-or-rollout-path>

Use the installed read-only analyzer with the exact native Codex session ID or
rollout JSONL path supplied by the user:

```text
python3 ~/.codex/codex_workflow/workflow.py analyze-thread \
  "<native-session-id-or-rollout-path>" --json
```

Report parent and child elapsed time, active turn time, completed and aborted
turns, models, reasoning efforts, token usage, model generations, compactions,
tool calls, child count, and maximum child concurrency. Token totals are the
native cumulative usage recorded at the end of each rollout; they are not an
invoice and do not include a price calculation.

The command never mutates sessions or configuration. A T3 thread identifier may
differ from the native Codex session ID, so if no rollout matches, ask for the
native ID or an explicit rollout file rather than guessing.
