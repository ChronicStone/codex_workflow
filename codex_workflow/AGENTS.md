<!-- codex-workflow-id: ChronicStone/codex_workflow -->
<!-- codex-workflow-managed-start -->
# Codex Workflow

Use Sol as the coordinator and Luna workers for bounded execution. Repository
instructions and routed skills remain authoritative for project-specific work.

## Core policy

- The coordinator owns intent, architecture, scope, cross-package contracts,
  integration, final claims, Git state, and user communication.
- Workers own only their assigned investigation, implementation, verification,
  review, or documentation surface.
- Fix the owning cause. Preserve unrelated work and never trade correctness or
  verification for lower token usage.
- Delegate only a coherent package with a clear outcome, owner, edit boundary,
  acceptance criteria, and evidence requirement. Use `fork_turns="none"` for
  initial workers and pass exact references instead of conversation history.
- Parallelize only independent work with non-overlapping mutable state. Do not
  create workers merely because capacity exists.
- Workers do not commit, push, publish, deploy, migrate shared systems, or take
  destructive actions unless the user explicitly authorized that operation.
- Automatic commits and automatic end-of-session workers are forbidden.

## Route selection

Choose the smallest route that completes the task. The user may override it.

- **Light:** questions, diagnosis, planning-only work, or small bounded changes.
  Work directly with no subagents.
- **Medium:** one bounded execution or investigation package benefits from Luna.
  Read `~/.codex/codex_workflow/medium_route.md`.
- **Heavy:** at least two substantial packages are independently executable, or
  implementation and independent acceptance need separate workers. Read
  `~/.codex/codex_workflow/heavy_route.md`.

Do not infer Heavy from task size alone. If ownership or architecture is still
uncertain, resolve it with the coordinator or one read-only scout before
allocating implementation.

## Project context

Load the repository's `AGENTS.md`, routed skills, and only the documentation
needed for the current package. Do not create a parallel documentation or
progress framework unless the project or user explicitly requests one.

## Completion

Integrate worker reports against the actual diff and current repository state.
Run or inspect the required owner and consumer gates, distinguish every form of
evidence precisely, and report incomplete checks honestly.
<!-- codex-workflow-managed-end -->

<!-- codex-workflow-project-personalization-start -->
<!-- codex-workflow-project-personalization-end -->

<!-- codex-workflow-project-local-instructions-start -->
<!-- codex-workflow-project-local-instructions-end -->
