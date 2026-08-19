# Changelog

All notable changes to `codex_workflow` are recorded here. Versions follow
Semantic Versioning.

## [2.3.1] - 2026-08-19

- Restored update compatibility with v2.2 launchers by keeping the persistent
  configuration on schema 6 and expressing Terra UI routing in the owned role
  templates instead of a new configuration key.

## [2.3.0] - 2026-08-19

- Routed bounded visible UI implementation and acceptance workers through Terra,
  while Sol retains product direction and final browser acceptance and Luna
  remains the default for non-visual worker packages.
- Added a configurable `ui_subagent_model` with a schema migration that preserves
  existing user configuration while defaulting UI roles to Terra.
- Made worker progress delivery deterministic with an exact canonical parent
  `progress_target`, a mandatory pre-action acknowledgement, and a heartbeat no
  later than 8 substantive tool calls since the previous checkpoint.
- Required Sol to relay received worker checkpoints before its next wait or task
  tool call, and to take over UI work after one unsuccessful Terra repair cycle.

## [2.2.0] - 2026-08-18

- Added progressive Medium and Heavy checkpoints for material evidence,
  decisions, coherent slices, verification boundaries, and blockers.
- Added a bounded heartbeat after 12 substantive tool calls without a semantic
  update, with worker messages capped at 60 words.
- Made Sol relay native worker updates promptly while preserving event-driven
  waits, delegated-surface isolation, and worker execution continuity.
- Kept checkpoints focused on evidence, rationale, and next actions without
  exposing private chain-of-thought, full logs, or routine tool narration.

## [2.1.0] - 2026-08-18

- Added spawn-first Heavy routing and an explicit Medium admission guard so a
  one-worker route cannot be mistaken for parallel execution.
- Made worker owner and surface immutable across follow-ups, replaced routine
  polling with event-driven waiting, and limited interrupts to invalid work.
- Kept Sol outside delegated surfaces until integration and split Luna effort:
  implementation roles use `xhigh`, while support roles use `high`.
- Added `analyze-thread`, a read-only native rollout analyzer for timing,
  concurrency, model, token, compaction, and tool-call evidence.
- Added this changelog and made changelog updates part of the release process.

## [2.0.5] - 2026-08-18

- Preserved mutable workflow configuration across release updates and hardened
  tagged release asset publication.

## [2.0.4] - 2026-08-18

- Supported global updates launched by older installed workflow versions.

## [2.0.3] - 2026-08-18

- Made workflow updates global by default instead of treating the current
  repository as an installation target.

## [2.0.2] - 2026-08-18

- Added opt-in Light, Medium, and Heavy routing, bounded Luna worker roles,
  evidence reuse, milestone validation, and global lifecycle configuration.

[2.3.1]: https://github.com/ChronicStone/codex_workflow/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/ChronicStone/codex_workflow/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/ChronicStone/codex_workflow/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.5...v2.1.0
[2.0.5]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.4...v2.0.5
[2.0.4]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.3...v2.0.4
[2.0.3]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.2...v2.0.3
[2.0.2]: https://github.com/ChronicStone/codex_workflow/releases/tag/v2.0.2
