<!-- codex-workflow-user-id: viettran-edgeAI/codex_workflow -->
<!-- codex-workflow-version: 1.1.0 -->
<!-- codex-workflow-user-managed-start -->
# AGENTS.md

When the user's trimmed message matches one of the following command forms,
read and follow the corresponding guide. Forms without placeholders must match
exactly.

- codex_workflow --install
  Guide:  ~/.codex/codex_workflow/install.md.

- codex_workflow --update
  Guide:  ~/.codex/codex_workflow/update.md.

- codex_workflow --update --source <PACKAGE>
  Match only when `<PACKAGE>` is one non-empty local path, optionally quoted.
  Pass that path to ~/.codex/codex_workflow/update.md as the selected local
  source. Reject missing paths or additional arguments.

- codex_workflow --check-update
  Guide:  ~/.codex/codex_workflow/check_update.md.

- codex_workflow --configure
  Guide: ~/.codex/codex_workflow/configuration_guide.md.

- codex_workflow --personal
  Guide: ~/.codex/codex_workflow/personalization_guide.md.

- codex_workflow --disable
  Guide: ~/.codex/codex_workflow/disable.md.

- codex_workflow --enable
  Guide: ~/.codex/codex_workflow/enable.md.
<!-- codex-workflow-user-managed-end -->
