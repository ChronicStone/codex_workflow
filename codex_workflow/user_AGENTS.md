<!-- codex-workflow-user-id: viettran-edgeAI/codex_workflow -->
<!-- codex-workflow-version: 1.1.1 -->
<!-- codex-workflow-user-managed-start -->
# AGENTS.md

Once at the start of every new session, before normal task work, run
`python3 ~/.codex/codex_workflow/workflow.py auto-check-update --json`, using
the equivalent Python 3.10+ invocation and path for the current platform. Run
it at most once per session.
The package default is disabled, so this command stays local and reports
`disabled` until the user explicitly enables update checks. If it reports
`update available`, notify the user briefly with the installed and available
versions. Stay quiet for `current` or `disabled`. Treat a check failure as a
non-blocking warning and continue the user's task.

When the user's trimmed message matches one of the following command forms,
read and follow the corresponding guide. Forms without placeholders must match
exactly.

- codex_workflow --install
  Guide:  ~/.codex/codex_workflow/install.md.

- codex_workflow --update
  Guide:  ~/.codex/codex_workflow/update.md.

- codex_workflow --check-update
  Guide:  ~/.codex/codex_workflow/check_update.md.

- codex_workflow --remove
  Guide: ~/.codex/codex_workflow/remove.md.

- codex_workflow --enable_auto_update
  Guide: ~/.codex/codex_workflow/enable_auto_update.md.

- codex_workflow --disable_auto_update
  Guide: ~/.codex/codex_workflow/disable_auto_update.md.

- codex_workflow --disable_auto_check_update
  Guide: ~/.codex/codex_workflow/disable_auto_check_update.md (legacy alias).

- codex_workflow --configure
  Guide: ~/.codex/codex_workflow/configuration_guide.md.

- codex_workflow --personal
  Guide: ~/.codex/codex_workflow/personalization_guide.md.

- codex_workflow --disable
  Guide: ~/.codex/codex_workflow/disable.md.

- codex_workflow --enable
  Guide: ~/.codex/codex_workflow/enable.md.
<!-- codex-workflow-user-managed-end -->
