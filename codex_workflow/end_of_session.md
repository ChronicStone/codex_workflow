# End-of-Session Handoff

Run this procedure only when the user directly commands the exact phrase
`end this session`, ignoring capitalization and surrounding punctuation. It is
shared by Medium and Heavy routes.

## Procedure

1. In Heavy route, collect checkpoints only from running or incomplete
   workers. Medium route has no worker checkpoint step.
2. Confirm that verification occurred after the last relevant code or test
   change. Do not rerun checks solely because the session is ending.
3. Complete warranted durable documentation before the handoff. In Heavy
   route, an existing `doc-writer` thread may perform compact read-only
   integrity checks; do not spawn one solely for status checks. Update
   `agent_docs/project_diary.md` only for significant decisions or durable
   lessons.
4. If meaningful files changed and the Explorer companion is available, ask it
   for a compact read-only closure audit covering changed files and line totals,
   diff errors, large or generated payloads, unexpected changed surfaces,
   blockers or deferrals, and verification evidence invalidated by later
   changes. It must not rerun tests or replace central correctness review. Keep
   the brief within 150 words. If Explorer is unavailable, perform the necessary
   checks directly and report the limitation.
5. Determine the deployment-plan state before updating the two main-owned
   status files:
   - when the plan is complete, with no pending work, blockers, or next action,
     record any lasting decisions in `agent_docs/project_diary.md`, then clear
     both `agent_docs/project_progress.md` and
     `agent_docs/latest_session_work.md`; keep both files present and empty;
   - when the plan is incomplete, reconcile
     `agent_docs/project_progress.md` with final status, verification evidence,
     blockers, and the next action when its recorded state changed, then
     replace `agent_docs/latest_session_work.md` once with changes,
     verification, pending work, blockers, and the next entry point;
   - when there is no active deployment plan, do not infer completion or clear
     existing status content without an explicit user request.
6. After those predictable documentation writes, run only compact checks that
   cover them. Broaden inspection only on failure or unexpected scope.
7. If meaningful project files changed, run `git add .`, then commit quietly
   with `git commit --quiet -m "[auto commit] <summary>"`. Report the one-line
   commit identity and any remaining dirty state.

If no meaningful project files changed and no completed-plan cleanup is
required, do not refresh `agent_docs/latest_session_work.md` and do not create
an empty commit.

Leave honest status, bounded changes, current verification, preserved user
work, and a clear continuation point.
