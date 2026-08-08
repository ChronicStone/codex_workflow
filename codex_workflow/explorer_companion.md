# Explorer Companion

Use one persistent read-only Explorer as the main agent's supporting-context
assistant throughout a deployment session.

## Role

- Main agent owns core work, priorities, decisions, critical evidence, edits,
  verification claims, and user communication.
- Explorer investigates peripheral or unfamiliar source, documentation,
  libraries, tools, dependencies, configuration, logs, and related context.
- Explorer retains useful findings, cross-references earlier evidence, and
  returns concise briefs with exact source locations.
- Explorer supports main-agent judgment; it does not replace decision-critical
  review.

## Lifecycle

- On first entering `deployment state`, spawn one Explorer with
  `agent_type="explorer"`, `task_name="explorer_companion"`, and
  `fork_turns="none"`.
- Brief it on the session goal, route, known decisions, and material constraints.
- Reuse the same thread across Medium and Heavy routes for the session.
- Do not create work merely to keep it active, create a second Explorer, or
  replace it. If unavailable, continue without it and report the limitation.

Explorer is a companion, not a task worker. Report it separately in usage
statistics, but count its live thread against platform concurrency. Count only
substantive requests, excluding initialization or acknowledgment-only exchanges.

## Scope

Use Explorer for supporting or context-heavy investigation. The main agent
directly reviews foundational project documents, core modules, critical
integration boundaries, and evidence that determines a decision.

Explorer may follow relevant adjacent sources but remains read-only. It must not
modify files, configuration, dependencies, Git state, or the environment;
implement fixes; edit tests or documentation; or make final decisions.
