"""Project entry-point, personalization, and documentation operations."""

from __future__ import annotations

from pathlib import Path

from . import ENTRY_FORMAT_VERSION, RUNTIME_SCHEMA_VERSION
from .errors import ValidationError
from .layout import PROJECT_ID, PackageLayout, ProjectPaths
from .markers import (
    PROJECT_LOCAL,
    PROJECT_PERSONALIZATION,
    WORKFLOW_MANAGED,
    extract,
    render_project_entry,
    replace,
)
from .personalization import materialize_personalization
from .plan import OperationPlan, json_mutation, read_json, text_mutation
from .transaction import Mutation


def plan_project_install(package: PackageLayout, project: ProjectPaths) -> OperationPlan:
    active_exists = project.active.exists()
    disabled_exists = project.disabled.exists()
    if active_exists and disabled_exists:
        raise ValidationError("both active and disabled project entry points exist")
    template = package.project_template.read_text(encoding="utf-8")
    personalization = (
        project.personalization.read_text(encoding="utf-8")
        if project.personalization.is_file()
        else package.default_personalization.read_text(encoding="utf-8")
    )
    direct_personalization = materialize_personalization(personalization)
    mutations: list[Mutation] = []
    warnings: list[str] = []
    entry_path = project.disabled if disabled_exists else project.active
    enabled = not disabled_exists
    if active_exists or disabled_exists:
        current = entry_path.read_text(encoding="utf-8")
        if PROJECT_ID in current:
            if WORKFLOW_MANAGED.start not in current or PROJECT_LOCAL.start not in current:
                raise ValidationError(
                    "legacy workflow entry point requires update migration before installation"
                )
            extract(current, WORKFLOW_MANAGED)
            current_personalization = extract(current, PROJECT_PERSONALIZATION)
            extract(current, PROJECT_LOCAL)
            if not project.personalization.is_file() and current_personalization:
                raise ValidationError(
                    "personalization resource is missing but the generated region is not empty"
                )
            if current_personalization != direct_personalization:
                raise ValidationError(
                    "project personalization resource and generated entry point disagree; "
                    "run codex_workflow --personal or codex_workflow --update"
                )
            if extract(current, WORKFLOW_MANAGED) != extract(template, WORKFLOW_MANAGED):
                raise ValidationError(
                    "recognized project entry point uses an older or modified workflow template; "
                    "run codex_workflow --update"
                )
        else:
            if disabled_exists:
                raise ValidationError("unrecognized disabled entry point cannot be imported")
            reject_reserved_markers(current)
            rendered = render_project_entry(
                template,
                personalization=direct_personalization,
                local_instructions=current,
            )
            mutations.append(text_mutation(entry_path, rendered))
            warnings.append("existing AGENTS.md will be preserved in the project-local region")
    else:
        rendered = render_project_entry(template, personalization=direct_personalization)
        mutations.append(text_mutation(project.active, rendered))
    if not project.personalization.is_file():
        mutations.append(text_mutation(project.personalization, personalization))
    created_docs: list[str] = []
    for source in sorted(package.project_docs.glob("*.md")):
        target = project.docs / source.name
        if not target.exists():
            mutations.append(Mutation(target, source.read_bytes()))
            created_docs.append(source.name)
    project_state = {
        "schema_version": RUNTIME_SCHEMA_VERSION,
        "entry_format_version": ENTRY_FORMAT_VERSION,
        "workflow_version": package.version,
        "enabled": enabled,
    }
    mutations.append(json_mutation(project.state, project_state))
    actions = []
    if created_docs:
        actions.append(
            {
                "role": "doc-writer",
                "action": "initialize newly copied project documents",
                "files": created_docs,
            }
        )
    return OperationPlan("project-install", mutations, warnings, actions)


def plan_personalize(project: ProjectPaths, resource_text: str) -> OperationPlan:
    entry = recognized_entry(project)
    current = entry.read_text(encoding="utf-8")
    if WORKFLOW_MANAGED.start not in current or PROJECT_LOCAL.start not in current:
        raise ValidationError("project entry point uses the legacy marker format")
    rendered = replace(
        current,
        PROJECT_PERSONALIZATION,
        materialize_personalization(resource_text),
    )
    return OperationPlan(
        "personalize",
        [
            text_mutation(project.personalization, resource_text),
            text_mutation(entry, rendered),
        ],
        [],
        [],
    )


def plan_enable(project: ProjectPaths, *, enable: bool) -> OperationPlan:
    source = project.disabled if enable else project.active
    target = project.active if enable else project.disabled
    operation = "enable" if enable else "disable"
    if target.is_file() and not source.exists():
        text = target.read_text(encoding="utf-8")
        if PROJECT_ID not in text:
            raise ValidationError(f"existing {target} is not workflow-owned")
        return OperationPlan(operation, [], [f"project is already {operation}d"], [])
    if not source.is_file() or target.exists():
        raise ValidationError("project entry-point state is missing or conflicted")
    content = source.read_bytes()
    if PROJECT_ID.encode() not in content:
        raise ValidationError("source project entry point is not workflow-owned")
    state = read_json(project.state, default={})
    state.setdefault("schema_version", RUNTIME_SCHEMA_VERSION)
    state.setdefault("entry_format_version", ENTRY_FORMAT_VERSION)
    state["enabled"] = enable
    return OperationPlan(
        operation,
        [Mutation(target, content), Mutation(source, None), json_mutation(project.state, state)],
        [],
        [],
    )


def plan_project_update(
    installed: PackageLayout,
    incoming: PackageLayout,
    project: ProjectPaths,
    *,
    legacy_local_instructions: str | None,
) -> tuple[list[Mutation], list[str]]:
    active_exists = project.active.exists()
    disabled_exists = project.disabled.exists()
    if active_exists and disabled_exists:
        raise ValidationError("both active and disabled project entry points exist")
    if not active_exists and not disabled_exists:
        return [], ["current project has no workflow entry point; user-level update only"]
    entry = project.disabled if disabled_exists else project.active
    current = entry.read_text(encoding="utf-8")
    if PROJECT_ID not in current:
        raise ValidationError("current project AGENTS.md is not workflow-owned")
    personalization_resource = (
        project.personalization.read_text(encoding="utf-8")
        if project.personalization.is_file()
        else incoming.default_personalization.read_text(encoding="utf-8")
    )
    direct = materialize_personalization(personalization_resource)
    if WORKFLOW_MANAGED.start in current and PROJECT_LOCAL.start in current:
        installed_template = installed.project_template.read_text(encoding="utf-8")
        if extract(current, WORKFLOW_MANAGED) != extract(
            installed_template, WORKFLOW_MANAGED
        ):
            raise ValidationError(
                "workflow-managed project region has local drift; move project rules to the local region"
            )
        if not project.personalization.is_file() and extract(
            current, PROJECT_PERSONALIZATION
        ):
            raise ValidationError(
                "personalization resource is missing but the generated region is not empty"
            )
        local = extract(current, PROJECT_LOCAL)
    else:
        old_template = installed.project_template.read_text(encoding="utf-8")
        current_without_personalization = replace(current, PROJECT_PERSONALIZATION, "")
        old_without_personalization = replace(old_template, PROJECT_PERSONALIZATION, "")
        if current_without_personalization != old_without_personalization:
            if legacy_local_instructions is None:
                raise ValidationError(
                    "legacy project entry contains local edits; pass reviewed local instructions explicitly"
                )
            reject_reserved_markers(legacy_local_instructions)
            local = legacy_local_instructions
        else:
            local = legacy_local_instructions or ""
    rendered = render_project_entry(
        incoming.project_template.read_text(encoding="utf-8"),
        personalization=direct,
        local_instructions=local,
    )
    mutations = [text_mutation(entry, rendered)]
    if not project.personalization.is_file():
        mutations.append(text_mutation(project.personalization, personalization_resource))
    state = {
        "schema_version": RUNTIME_SCHEMA_VERSION,
        "entry_format_version": ENTRY_FORMAT_VERSION,
        "workflow_version": incoming.version,
        "enabled": not disabled_exists,
    }
    mutations.append(json_mutation(project.state, state))
    return mutations, []


def recognized_entry(project: ProjectPaths) -> Path:
    if project.active.exists() and project.disabled.exists():
        raise ValidationError("both active and disabled project entry points exist")
    path = project.active if project.active.is_file() else project.disabled
    if not path.is_file() or PROJECT_ID not in path.read_text(encoding="utf-8"):
        raise ValidationError("no recognized workflow project entry point")
    return path


def reject_reserved_markers(text: str) -> None:
    reserved = [
        WORKFLOW_MANAGED.start,
        WORKFLOW_MANAGED.end,
        PROJECT_PERSONALIZATION.start,
        PROJECT_PERSONALIZATION.end,
        PROJECT_LOCAL.start,
        PROJECT_LOCAL.end,
    ]
    collisions = [marker for marker in reserved if marker in text]
    if collisions:
        raise ValidationError(f"existing AGENTS.md contains reserved markers: {collisions}")
