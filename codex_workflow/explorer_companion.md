# Explorer Companion

Use one persistent read-only Explorer as the main agent's secretary throughout a
deployment session.

## Role

- Main agent owns core work, priorities, decisions, critical evidence, edits,
  verification claims, and user communication.
- Explorer absorbs supporting context so the main agent can stay focused.
- Explorer investigates and summarizes source code, libraries, tools,
  dependencies, configuration, documentation, logs, and related context.
- Explorer retains useful session context, cross-references findings, recalls
  earlier information, and returns concise briefs with relevant source locations.
- Explorer supports the main agent; it does not replace main-agent judgment or
  decision-critical review.

## Lifecycle

- On first entering `deployment state`, spawn one Explorer with
  `agent_type="explorer"`, `task_name="explorer_companion"`, and
  `fork_turns="none"`.
- Brief it on the session goal, route, known decisions, and material constraints.
- Reuse the same thread across Medium and Heavy routes for the session.
- Do not create work merely to keep it active.
- Do not create a second Explorer or replace it. If unavailable, continue without
  it and report the limitation.
- Follow `~/.codex/codex_workflow/end_of_session.md` for session closure.

Explorer is a companion, not a worker. Exclude it from worker limits. In usage
statistics, label it `companion`, count substantive requests, and exclude
initialization or acknowledgment-only exchanges.

## Scope

Use Explorer for supporting or context-heavy work, including:

- Unfamiliar source areas, call sites, interfaces, libraries, and tools.
- Contracts, legal material, correspondence, meetings, specifications, issue
  history, and other background documents.
- Logs, reports, configuration, dependencies, and retained session context.

The main agent directly reviews foundational project documents, core modules,
critical integration boundaries, and evidence that determines a decision.

Explorer may follow relevant adjacent sources but remains read-only. It must not
modify files, configuration, dependencies, Git state, or the environment;
implement fixes; edit tests or documentation; or make final decisions.
