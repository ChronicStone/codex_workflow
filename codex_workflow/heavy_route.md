# Heavy Route

<!-- codex-workflow-effective-config-start -->
## Effective Workflow Configuration

- Default executor: `implementer` (`xhigh` reasoning effort).
- Implementation workers: `gpt-5.6-luna` (`xhigh` reasoning effort).
- UI workers: `gpt-5.6-terra` (`xhigh` implementation, `high` review reasoning effort).
- Support workers: `gpt-5.6-luna` (`high` reasoning effort).
- Enabled workers: `scout`, `implementer`, `ui-implementer`, `tester`, `reviewer`, `ui-reviewer`, `doc-writer`.
- Maximum concurrent child workers: `4`.
- Cumulative task worker budget: `6` total workers.
- Maximum worker final-report package: `200` words.

Create only enabled workers and obey these limits.
<!-- codex-workflow-effective-config-end -->

The coordinator owns architecture, dependency order, cross-package contracts,
integration gates, Git, final status, and user communication. Workers own only
their bounded operational context.

## Allocation

Use a spawn-first sequence. Read only enough to identify ownership boundaries,
dependencies, and protected state, then dispatch all 2-4 independent initial
workers before Sol begins deep repository investigation. If ownership is
uncertain, one read-only scout may resolve it first; allocate implementation
immediately after that report. When the task cannot support two independent
packages, report a Heavy route mismatch instead of manufacturing concurrency or
placing sequential stages in parallel.

Use `scout` only when a bounded read-only investigation will prevent multiple
workers from repeating discovery. It is not persistent and must not become a
mandatory gateway.

Allocate 2-4 initial workers only for independently completable ownership
packages, not by file count, and never exceed the cumulative task budget. Two
workers may run concurrently only when neither one's output or mutable state
can change the other's work. Shared build output, generated files, fixtures,
databases, ports, browsers, devices, or overlapping files make work sequential.

Use `implementer` for general production work and `ui-implementer` for visible
frontend work. Add an independent tester or reviewer only when the user asks or
a concrete risk requires it, such as security, infrastructure, migrations,
public contracts, concurrent integration, or rendered acceptance. It validates
the uncovered risk and does not rerun the implementer's fresh passing suite.
Reuse the responsible implementer for repairs and do not repeat scouts or
reviewers over the same surface. Use `reviewer` for correctness and architecture
review, and `ui-reviewer` for rendered interaction and visual acceptance. A UI
reviewer must inspect the running product and cannot be replaced by code review.

For visible UI, Sol defines the intended hierarchy, interaction behavior,
responsive contract, and design-system constraints before allocation. Terra UI
workers may run in parallel only on independent rendered experiences with no
shared component, state, browser, port, or visual contract. Sol inspects the
integrated rendered flow and owns final visual and UX acceptance. Open-ended
design exploration and major redesigns stay with Sol; after one Terra repair
cycle still leaves substantial defects, Sol takes over instead of delegating
again.

Keep hard architecture, security, migration, concurrency, and cross-cutting
decisions with the Sol coordinator. Do not spawn another Sol instance; give a
Luna implementer an explicit execution guide after the coordinator resolves the
decision.

## Capsules

Every initial worker uses `fork_turns="none"` and receives:

- task ID, outcome, owner, exact edit or read surface, and protected areas;
- `progress_target` equal to the exact canonical parent task path;
- relevant decisions, interfaces, dependencies, and exact references;
- recommended approach and why it fits;
- the most important invariant and likely integration pitfall;
- acceptance criteria, required verification, and regression boundary;
- escalation conditions and a final report capped by the configured limit.

Use `<role> — <task ID>` in commentary, plans, worker ledgers, and final
reports, keyed by native `agent_id`. Never use a generated person nickname
except when quoting a native platform error, and do not invent `nickname` or
`display_name` configuration.

At dispatch, publish a worker ledger with every worker's scope, expected
outcome, and first milestone. Before its first repository or task tool call, each
worker must call `send_message` with `target` equal to `progress_target`,
acknowledge the capsule, and state its first action. It sends progress checkpoints
at the first material evidence, a material decision or approach change,
completion of a coherent slice, before and after long verification, and any
blocker. After 8 substantive tool calls since the last checkpoint, it sends a
compact heartbeat. Each update stays under 60 words and states evidence, the
current decision and why, the next action, and blockers without raw chain-of-
thought, full logs, or routine tool narration. Workers continue immediately
after sending; acknowledgement is not required. A missing or unusable
`progress_target` makes the capsule invalid. Relay every received checkpoint in
commentary before the next wait or task tool call. Combine checkpoints that are
already available into one readable update, but do not wait to manufacture a
batch.

The capsule owner and surface are immutable. Follow-ups can clarify facts or
repair a failed criterion inside the same boundary; work that adds a feature,
owner, package, or acceptance surface requires a new allocation decision within
the remaining task budget.

For delegated implementation, include an ordered execution guide with
prerequisites, named files or symbols, the milestone where a focused check
should first pass, the single owner gate required at handoff, edge cases,
forbidden changes, and any final integration gate. Do not schedule broad checks
for knowingly broken
intermediate states or make workers rediscover established decisions.

## Evidence and repair

Reports contain the outcome, changed contracts, new facts, invalidated
assumptions, exact verification method, residual risk, decision required, and
exact references. Store large logs and artifacts outside the report.

Assign each gate to exactly one worker. Record its command, scope, result, and
the scoped input revision. Reuse a passing result while those inputs remain
unchanged. After a failure, diagnose and change a relevant input before retrying
the same command. If a final readiness gate subsumes owner checks, run only the
readiness gate at that point.

When verification finds a production defect, the coordinator sends a compact
defect packet to the responsible implementer: failed criterion, reproduction,
observed versus expected behavior, affected contract, exact evidence, and scope
impact. Escalate repeated failures or any repair that changes ownership,
architecture, public contracts, security, migration risk, or authority.

Wait for lifecycle or progress events with one long native wait between events
instead of polling. Relay checkpoints promptly, then return to waiting. Queue
new facts for the next worker boundary and interrupt only when
continuing became invalid, destructive, or unauthorized. Sol stays out of each
delegated read and edit surface until its report unless a blocking architecture
decision requires coordinator input. If the user explicitly requests immediate push, deploy, or ship,
stop optional delegation and checks, spawn no new workers, keep Sol responsible
for the authorized irreversible action, and allow at most one existing
read-only Luna monitor. Before completion, inspect the integrated diff and
current state, confirm evidence freshness, and report every unrun or blocked
gate. Never run an automatic documentation sweep, session closure, or commit.
