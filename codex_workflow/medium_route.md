# Medium Route

Use exactly one configured worker when delegation saves coordinator context or
gives a useful independent execution boundary. Never create a replacement worker
for the same Medium task; follow-up turns reuse the initial worker. The coordinator
remains responsible for the plan, architecture, integration assurance, Git,
and communication. The worker owns focused and affected-owner checks; the
coordinator consumes that evidence and runs only a missing integration or
explicit final shipping gate.

Medium has no worker parallelism: the maximum concurrency is one even when the
platform allows more. Before dispatch, confirm the requested outcome fits one
stable owner and surface. If two or more independently completable packages are
needed for speed, surface the route mismatch and recommend Heavy; do not hide
multiple packages in a broad Medium capsule.

Choose the role by the actual package:

- `scout` for bounded read-only discovery or root-cause evidence;
- `implementer` for backend, full-stack, library, automation, or configuration;
- `ui-implementer` for visible frontend work requiring browser verification;
- `tester` for an independent verification package;
- `reviewer` or `ui-reviewer` for an explicit independent acceptance pass;
- `doc-writer` for a targeted durable documentation update.

For visible UI, Sol first states the intended hierarchy, interaction behavior,
responsive contract, and design-system constraints. The Terra `ui-implementer`
then owns the bounded implementation and browser evidence; after its report, Sol
inspects the integrated rendered flow and owns final visual and UX acceptance.
Open-ended design exploration or a major redesign stays with Sol. If one Terra
repair cycle still leaves substantial defects, Sol takes over the surface.

Spawn the worker with `fork_turns="none"`. Its capsule must include the task ID,
`progress_target` set to the exact canonical parent task path, outcome, owner and
exact surface, protected areas, relevant decisions and references, recommended
approach, important invariant, likely
pitfall, acceptance criteria, required checks, escalation conditions, and
concise return format. Use `<role> — <task ID>` in commentary, plans, worker
ledgers, and reports, keyed by native `agent_id`; generated person nicknames are
reserved for quoted native platform errors.

At dispatch, tell the user the worker's scope, expected outcome, and first
milestone. Before its first repository or task tool call, the worker must call
`send_message` with `target` equal to `progress_target`, acknowledge the capsule,
and state its first action. It sends progress checkpoints at the first material
evidence, a material decision or approach change, completion of a coherent slice,
before and after long verification, and any blocker. After 8 substantive tool
calls since the last checkpoint, it sends a compact heartbeat. Each update stays
under 60 words and states evidence, the current decision and why, the next action,
and blockers without raw chain-of-thought, full logs, or routine tool narration.
The worker continues immediately after sending it; acknowledgement is not
required. A missing or unusable `progress_target` makes the capsule invalid.

The capsule owner and surface remain fixed for the entire task. Follow-ups may
send changed facts, answer a question, or request a repair against an existing
acceptance criterion, but they cannot add another feature, owner, package, or
verification surface. Re-route work that crosses that boundary.

Inspect the worker's evidence and resulting diff before integrating it. Treat a
passing command as fresh until its scoped inputs change, and never repeat it
only to obtain independent confirmation. Reopen only for conflict, stale
evidence, a missing integration boundary, or high risk. Use one long native wait
between lifecycle or progress events rather than coordinator polling loops or
repeated status turns. Relay checkpoints promptly and return to waiting. Queue
changed facts for the next worker boundary; interrupt only when its
current work became invalid, destructive, or unauthorized. Sol does not inspect
or edit the delegated surface before the report unless an unresolved
architecture decision blocks progress. Stop delegation when the remaining work
is smaller than a clean handoff.
