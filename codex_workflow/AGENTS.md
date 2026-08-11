<!-- codex-workflow-id: viettran-edgeAI/codex_workflow -->
<!-- codex-workflow-managed-start -->
# AGENTS.md

## Project Context


## Design Principles

- Keep modules cohesive, interfaces explicit, coupling minimal, and behavior
  testable, replaceable, and reusable.
- Define proportionate acceptance and verification before implementation. Keep
  related tests cohesive; never weaken coverage, assertions, or failure
  visibility to save time or tokens.
- Preserve unrelated user work and use verified facts in durable documentation.

Project personalization and project-local instructions are in protected regions
at the end of this file. They override conflicting workflow defaults, but not
higher-level instructions.

## Working State

- `deployment state`: planning or executing a broad, possibly multi-session
  deployment plan.
- `leaf state`: work outside that plan, including general questions and small,
  bounded edits or operations.

## Project Documentation

The durable project documents are under `agent_docs/`:

- `project_overview.md`: goals, architecture, workflow, and major decisions.
- `project_core_tech.md`: concise special technology or architecture notes.
- `project_structure.md`: layout, modules, components, and ownership.
- `project_progress.md`: goal, overall progress, current position, next milestone.
- `project_diary.md`: lasting decisions, discarded approaches, and lessons.
- `latest_session_work.md`: detailed handoff evidence and continuation point.
- Module-specific documents, when present.

`project_progress.md` and `latest_session_work.md` may be edited only in
`deployment state` or when the user explicitly requests it. The main agent owns
them during normal execution; the dedicated `end_of_session` worker owns them
during an invoked handoff. No other worker may edit them.

Keep raw logs, temporary reasoning, and short-lived checkpoints out of durable
documents. Never delete a main project document without warning the user and
receiving a second explicit confirmation.

## Route Selection

There are three routes:

- **Light**: leaf-state work. The main agent works directly; no subagents.
- **Medium**: deployment-state work performed by the main agent. Explorer and
  the dedicated End-of-Session worker are the only subagent exceptions. Read
  `~/.codex/codex_workflow/medium_route.md`.
- **Heavy**: deployment-state work orchestrated through specialized workers.
  Read `~/.codex/codex_workflow/heavy_route.md`.

The user selects the route for the session. If unspecified, use Light; do not
infer Medium or Heavy. Light implies `leaf state`; Medium and Heavy imply
`deployment state`. Keep the selected route until the user changes it or the
session ends.

## Context Loading

- In Light, inspect only material needed for the current task.
- On first entering deployment state, read the selected route and
  `explorer_companion.md`, then initialize the single persistent Explorer.
- Give Explorer the session goal, known constraints, investigation questions,
  and boundaries. It reads the foundational project documents and relevant
  repository context, then returns the planning brief defined in its contract.
- In Medium, the main agent uses that brief to narrow its direct implementation
  inspection. In Heavy, Explorer is the default gateway for repository,
  architecture, dependency, and external research; the main agent normally
  consumes the brief rather than repeating discovery.
- The main agent may inspect any critical source or evidence, but should do so
  only when it materially affects a decision, resolves uncertainty or
  contradiction, or validates a high-risk integration boundary.
- Resolve stale or conflicting project status with targeted evidence. Load only
  relevant module documentation and avoid replaying raw logs, large diffs,
  directory listings, or complete source files into the main context.

## Platform Paths

Workflow documents use `/` as a platform-neutral separator. Translate paths to
the current operating system and shell when running filesystem commands.
<!-- codex-workflow-managed-end -->

<!-- codex-workflow-project-personalization-start -->
<!-- codex-workflow-project-personalization-end -->

<!-- codex-workflow-project-local-instructions-start -->
<!-- codex-workflow-project-local-instructions-end -->
