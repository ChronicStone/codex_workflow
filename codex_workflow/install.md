# Workflow Installation

Use this procedure for the first manual installation and for
`codex_workflow --install` in another project. Copy files; never move or delete
the release package.

## Release package contract

Install from the universal GitHub Release ZIP asset, not from a repository
checkout. Use `codex_workflow-<version>.zip` on Linux, macOS, and Windows.
After extraction, the package root must contain exactly one directory:

```text
codex_workflow/
```

The release asset contains the complete runtime payload under that directory.
It does not contain `README.md`, README images, development documentation,
`.git/`, or other repository-only files. Do not read `README.md` as an
installation source.

Validate the package before copying anything:

- `codex_workflow/VERSION` contains one semantic version in `MAJOR.MINOR.PATCH`
  form, with an optional SemVer prerelease or build suffix;
- the `codex-workflow-version` marker in `user_AGENTS.md` matches `VERSION`;
- the release tag, after removing an optional leading `v`, matches `VERSION`;
- the selected ZIP asset is the matching release asset and its checksum matches
  `SHA256SUMS` when that release asset is available.

Release assets are extracted into a temporary directory. Keep the extracted
`codex_workflow/` directory unchanged while this procedure runs, and remove
only that temporary directory after verification.

## Package and targets

Normalize the package root to the directory containing `VERSION`, `AGENTS.md`,
`user_AGENTS.md`, `workflow_config.json`, `project_docs/`, `agents/`, both
route files, the Explorer companion, `end_of_session.md`, and all lifecycle and
command guides.

User-level targets:

    ~/.codex/AGENTS.md
    ~/.codex/agents/
    ~/.codex/codex_workflow/
    ~/.codex/codex_workflow/templates/AGENTS.md
    ~/.codex/codex_workflow/templates/agents/
    ~/.codex/codex_workflow/templates/project_docs/
    ~/.codex/codex_workflow/.source_backup/<version>/

Project-level targets:

    AGENTS.md
    .codex_workflow_hidden_resource/personalization.md
    agent_docs/

The disabled project entry point remains at
`.codex_workflow_hidden_resource/.AGENTS.md`.

On Windows, resolve `~/.codex/` through the current user's profile directory
and use the platform's normal path separator. The target layout and ownership
rules are otherwise the same.

## Validate first

Before writing, validate the semantic `VERSION`, user and project identity
markers, JSON schema, all six project-document templates, routes, Explorer
companion, End-of-Session runtime, guides, and every worker TOML. The version
in `user_AGENTS.md` must match `VERSION`.

If an existing project `AGENTS.md` does not have the project workflow marker,
offer exactly:

1. **Overwrite all** — confirm before replacing it.
2. **Merge** — ask which sections or passages to preserve, then merge only
   those parts into the workflow template.

Do not choose for the user. If both project entry points exist, stop and report
the conflict.

## First manual installation

Run these phases in order.

### 1. Copy the user-level package

1. Create the target directories.
2. Copy `VERSION`, `user_AGENTS.md`, all lifecycle guides, `configuration_guide.md`,
   `personalization_guide.md`, `medium_route.md`, `heavy_route.md`, and
   `explorer_companion.md`, and `end_of_session.md` into
   `~/.codex/codex_workflow/`.
3. Copy project `AGENTS.md` to
   `~/.codex/codex_workflow/templates/AGENTS.md`, copy every `agents/*.toml` to
   `~/.codex/codex_workflow/templates/agents/`, and copy all six
   `project_docs/*.md` templates to
   `~/.codex/codex_workflow/templates/project_docs/`.
4. Copy the complete normalized release package to
   `~/.codex/codex_workflow/.source_backup/<version>/`. Keep the original
   release package unchanged as an additional repair source.
5. Extract the body between
   `codex-workflow-user-managed-start/end` in `user_AGENTS.md`. If
   `~/.codex/AGENTS.md` exists, replace its matching managed body or append the
   marked block when no such block exists; preserve all other content. If it is
   absent, create it with the marked block and extracted body.

### 2. Install the default user-level runtime state

Copy the default `workflow_config.json` to
`~/.codex/codex_workflow/workflow_config.json` when missing. If a valid resource
already exists, preserve its values and add only missing defaults. Without
asking configuration questions, apply the final snapshot to Heavy route, the
enabled worker TOMLs, and workflow-owned platform settings. Configuration can
be changed later with `codex_workflow --configure`.

### 3. Install the current project

Run the project installation procedure below, including creation of the default
personalization resource and final `doc-writer` initialization.

## Project installation — `codex_workflow --install`

This command does not reinstall user-level files. Require a valid installed
user marker, workflow payload, configuration resource, project template, and
enabled worker set.

1. Resolve the entry point:
   - update recognized `AGENTS.md`;
   - if only `.codex_workflow_hidden_resource/.AGENTS.md` is recognized, keep
     the project disabled and update that file;
   - handle an unrecognized `AGENTS.md` with the two choices above.
2. If the project has no entry point, copy the installed template. If an entry
   point is already recognized, preserve it. For Merge, create the entry point
   from the workflow template plus only the content selected by the user.
3. Create `.codex_workflow_hidden_resource/personalization.md` from the default
   resource in `personalization_guide.md` when missing. For a new project, keep
   the template's personalization marker empty. For a recognized existing
   installation, preserve its resource and already-materialized marker content.
   Do not ask personalization questions. Personalization begins only when the
   user sends `codex_workflow --personal`.
4. Verify that only one entry point exists and that its enabled or disabled
   state has not changed unexpectedly.
5. Create `agent_docs/` and copy every missing document from
   `~/.codex/codex_workflow/templates/project_docs/`. Record the exact list of
   files created during this installation. Never replace an existing project
   document.
6. Always spawn one `doc-writer` subagent to initialize the Project
   Documentation Framework. Give it these requirements:
   - inspect the smallest project surface needed for verified initial context;
   - treat an empty or source-less project as a valid installation state; record
     that no implementation context was available instead of reporting a
     failure;
   - initialize only the documents recorded as newly copied in the preceding
     step and remove their `codex-workflow-bootstrap-template` markers;
   - this installation-scoped task may initialize newly copied
     `project_progress.md` and `latest_session_work.md`; this authority ends
     when installation finishes;
   - when no document was newly copied, perform only a read-only completeness
     check of the six-file framework;
   - preserve every project document that existed before this installation;
   - record only verified facts, use concise starter structure, and leave
     deployment status empty when no active plan or handoff exists;
   - do not edit either entry point, personalization, source code, Git state,
     or user-level files.
7. Verify that all six framework files exist and that newly copied templates no
   longer contain bootstrap markers. If the required `doc-writer` cannot be
   created or fails to initialize the framework, report installation
   as incomplete with its evidence; do not silently perform the subagent's
   work in the main thread.

## Completion checks

- `~/.codex/codex_workflow/` contains the installed guides, routes, Explorer
  companion, End-of-Session runtime, lifecycle documents, persistent
  configuration, project, worker, and documentation templates, `VERSION`, and
  source backup;
- Heavy route and active worker TOMLs match `workflow_config.json`;
- project entry points and route files do not read configuration or
  personalization guides/resources during normal project work;
- a new project has the default personalization resource and an empty
  personalization marker; an existing recognized installation retains its
  resource and materialized marker content;
- all six project documents exist and pre-existing documents are unchanged;
- user instructions, unrelated workers, unrelated Codex configuration, source
  packages, and backups are preserved.
