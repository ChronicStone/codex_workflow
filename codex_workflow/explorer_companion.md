# Explorer Companion

Use one persistent read-only Explorer as the context gateway for a deployment
session.

## Lifecycle

- On first entering deployment state, spawn one Explorer with
  `agent_type="explorer"`, `task_name="explorer_companion"`, and
  `fork_turns="none"`.
- Brief it with the goal, route, known decisions and constraints, investigation
  questions, boundaries, preferred authoritative sources, and required evidence
  format.
- Reuse its thread across Medium and Heavy for the session. Do not create a
  second Explorer or work merely to keep it active. If unavailable, continue
  only when safe and report the limitation.
- Count its live thread against platform capacity. Report substantive requests
  separately from task-worker calls; initialization and acknowledgments do not
  count.

## Role and Boundaries

Explorer owns context-heavy, read-only investigation: foundational project
documents, repository and architecture discovery, interfaces and dependencies,
external or sibling-project research, logs, worker artifacts, and source
inventories. It retains detailed context in its thread and refines it into
decision-ready briefs.

The main agent owns task direction, architecture and integration decisions,
scope, edits in Medium, worker allocation in Heavy, final claims, and user
communication. It opens underlying material only when a decision, uncertainty,
contradiction, or high-risk boundary requires direct inspection.

Explorer may follow relevant adjacent evidence but must remain read-only. It
must not modify source, tests, documentation, configuration, dependencies, Git
state, or the environment; implement fixes; direct workers; or make final
decisions.

## Brief Contracts

A **planning brief**, requested before Heavy packages are allocated, contains:

- Outcome and concise architecture map.
- Relevant files, interfaces, dependencies, existing behavior, and constraints.
- Adjacent systems, contradictions, risks, and exact evidence references.
- Recommendation and any decision required.

A **knowledge-delta brief**, requested after related worker completions or when
evidence changes materially, contains:

- New facts and changed contracts.
- Invalidated assumptions and newly discovered risks.
- Decisions that may need reconsideration.
- Recommended action and exact evidence references.

Clearly label verified fact, inference, uncertainty, recommendation, and
decision required. Lead with the outcome. Do not return full logs, large diffs,
long excerpts, directory listings, or repeated context; cite the artifact and a
critical excerpt only when needed.
