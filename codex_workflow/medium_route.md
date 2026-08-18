# Medium Route

Use exactly one Luna worker when delegation saves coordinator context or gives a
useful independent execution boundary. Never create a replacement worker for
the same Medium task; follow-up turns reuse the initial worker. The coordinator
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

Spawn the worker with `fork_turns="none"`. Its capsule must include the task ID
and state the outcome, owner and exact surface, protected areas, relevant
decisions and references, recommended approach, important invariant, likely
pitfall, acceptance criteria, required checks, escalation conditions, and
concise return format. Use `<role> — <task ID>` in commentary, plans, worker
ledgers, and reports, keyed by native `agent_id`; generated person nicknames are
reserved for quoted native platform errors.

The capsule owner and surface remain fixed for the entire task. Follow-ups may
send changed facts, answer a question, or request a repair against an existing
acceptance criterion, but they cannot add another feature, owner, package, or
verification surface. Re-route work that crosses that boundary.

Inspect the worker's evidence and resulting diff before integrating it. Treat a
passing command as fresh until its scoped inputs change, and never repeat it
only to obtain independent confirmation. Reopen only for conflict, stale
evidence, a missing integration boundary, or high risk. Use one long native wait
or background monitor rather than coordinator polling loops or repeated status
turns. Queue changed facts for the next worker boundary; interrupt only when its
current work became invalid, destructive, or unauthorized. Sol does not inspect
or edit the delegated surface before the report unless an unresolved
architecture decision blocks progress. Stop delegation when the remaining work
is smaller than a clean handoff.
