# Heavy Route

<!-- codex-workflow-effective-config-start -->
## Effective Workflow Configuration

- Default executor: `implementer` (`xhigh` reasoning effort).
- Default subagent model: `gpt-5.6-luna` (`xhigh` reasoning effort).
- Enabled workers: `scout`, `implementer`, `ui-implementer`, `tester`, `reviewer`, `ui-reviewer`, `doc-writer`.
- Maximum concurrent child workers: `4`.
- Maximum worker final-report package: `200` words.

Create only enabled workers and obey these limits.
<!-- codex-workflow-effective-config-end -->

The coordinator owns architecture, dependency order, cross-package contracts,
integration gates, Git, final status, and user communication. Workers own only
their bounded operational context.

## Allocation

Use `scout` only when a bounded read-only investigation will prevent multiple
workers from repeating discovery. It is not persistent and must not become a
mandatory gateway.

Allocate implementation by independently completable ownership, not by file
count. Two workers may run concurrently only when neither one's output or
mutable state can change the other's work. Shared build output, generated files,
fixtures, databases, ports, browsers, devices, or overlapping files make work
sequential.

Use `implementer` for general production work and `ui-implementer` for visible
frontend work. After self-check, use `tester` only when independent behavioral
verification adds value. Use `reviewer` for correctness and architecture review,
and `ui-reviewer` for rendered interaction and visual acceptance. A UI reviewer
must inspect the running product and cannot be replaced by code review.

Keep hard architecture, security, migration, concurrency, and cross-cutting
decisions with the Sol coordinator. Do not spawn another Sol instance; give a
Luna implementer an explicit execution guide after the coordinator resolves the
decision.

## Capsules

Every initial worker uses `fork_turns="none"` and receives:

- task ID, outcome, owner, exact edit or read surface, and protected areas;
- relevant decisions, interfaces, dependencies, and exact references;
- recommended approach and why it fits;
- the most important invariant and likely integration pitfall;
- acceptance criteria, required verification, and regression boundary;
- escalation conditions and a final report capped by the configured limit.

For Luna implementation, include an ordered execution guide with prerequisites,
named files or symbols, focused checks after coherent stages, edge cases,
forbidden changes, and a final validation ladder. Do not make workers rediscover
decisions already established by the coordinator.

## Evidence and repair

Reports contain the outcome, changed contracts, new facts, invalidated
assumptions, exact verification method, residual risk, decision required, and
exact references. Store large logs and artifacts outside the report.

When verification finds a production defect, the coordinator sends a compact
defect packet to the responsible implementer: failed criterion, reproduction,
observed versus expected behavior, affected contract, exact evidence, and scope
impact. Escalate repeated failures or any repair that changes ownership,
architecture, public contracts, security, migration risk, or authority.

Wait for lifecycle events instead of polling. Before completion, inspect the
integrated diff and current state, confirm evidence freshness, and report every
unrun or blocked gate. Never run an automatic documentation sweep or commit.
