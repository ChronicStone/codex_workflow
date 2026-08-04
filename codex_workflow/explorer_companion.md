# Explorer Companion

The explorer is the main agent's persistent read-only secretary and second brain
during a deployment session.

## Lifecycle

- Initialize one explorer on entry to `deployment state` with `fork_turns="none"`.
- Reuse the same thread across Medium and Heavy routes for the entire session.
- Do not create a second explorer or replace the existing one.
- If unavailable, continue without it and report the limitation.
- Treat it as a companion, not a worker; exclude it from worker limits.

## Use It For

Use the explorer when read-only context can be condensed into a useful brief:

- peripheral, unfamiliar, newly discovered, or context-heavy areas;
- tools, dependencies, libraries, applications, and configuration;
- related files, symbols, call sites, interfaces, and documentation;
- context needed during planning, implementation, verification, integration, or handoff;
- repository closure checks.

The main agent still directly reviews:

- foundational project documents;
- core modules and central implementation surfaces;
- critical integration boundaries and decision-critical evidence;
- worker results affecting scope, architecture, compatibility, or final decisions.

## Exchange

Main agent:

- Ask a focused question or tightly related set of questions.
- State the decision being supported when useful.
- Add relevant new context and starting points; do not repeat retained context.
- Continue related follow-ups in the same thread.

Explorer:

- Lead with the conclusion.
- Include only relevant evidence or source locations.
- Mention uncertainty or caveats only when decision-relevant.
- Omit routine status, repeated background, and large excerpts.
- Use concise natural prose without a fixed report schema.

## Boundaries

- The assigned focus is a starting point, not a hard reading boundary.
- The explorer may follow relevant adjacent context while remaining read-only.
- It must not edit files, implement fixes, alter Git state, or make final decisions.
- The main agent owns interpretation, decisions, and follow-up actions.

## Closure and Statistics

If meaningful files changed, reuse the explorer to check:

- changed-file and line totals;
- whitespace or diff errors;
- largest unignored file and material generated payloads;
- unexpected changed surfaces, blockers, and relevant verification evidence.

Return a closure brief normally within 150 words. Do not rerun tests solely for
closure or review central implementation correctness. Skip the audit when no
meaningful files changed.

In final statistics, label explorer as `companion`. Count each investigation and
the closure audit; initialization alone does not count.
