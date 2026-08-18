# Changelog

All notable changes to `codex_workflow` are recorded here. Versions follow
Semantic Versioning.

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

[2.1.0]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.5...v2.1.0
[2.0.5]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.4...v2.0.5
[2.0.4]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.3...v2.0.4
[2.0.3]: https://github.com/ChronicStone/codex_workflow/compare/v2.0.2...v2.0.3
[2.0.2]: https://github.com/ChronicStone/codex_workflow/releases/tag/v2.0.2
