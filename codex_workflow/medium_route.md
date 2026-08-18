# Medium Route

Use exactly one Luna worker when delegation saves coordinator context or gives a
useful independent execution boundary. Never create a replacement worker for
the same Medium task; follow-up turns reuse the initial worker. The coordinator
remains responsible for the plan, architecture, integration assurance, Git,
and communication. The worker owns focused and affected-owner checks; the
coordinator consumes that evidence and runs only a missing integration or
explicit final shipping gate.

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

Inspect the worker's evidence and resulting diff before integrating it. Treat a
passing command as fresh until its scoped inputs change, and never repeat it
only to obtain independent confirmation. Reopen only for conflict, stale
evidence, a missing integration boundary, or high risk. Use one long native wait
or background monitor rather than coordinator polling loops or repeated status
turns. Routine follow-ups contain only changed facts, the failed criterion, and
the next action. Stop delegation when the remaining work is smaller than a
clean handoff.
