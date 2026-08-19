"""Regression tests for the lifecycle runtime."""

from __future__ import annotations

import json
import contextlib
import io
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "codex_workflow"
PACKAGE_VERSION = (PACKAGE / "VERSION").read_text(encoding="utf-8").strip()

import sys

sys.path.insert(0, str(PACKAGE))

import workflow as workflow_cli

from runtime.analyze import analyze_thread
from runtime.config import (
    WorkflowConfig,
    patch_codex_config,
    remove_workflow_owned_config,
    render_heavy_route,
    render_worker_template,
)
from runtime.backup import append_backup_mutations
from runtime.errors import TransactionError, ValidationError
from runtime.lifecycle import (
    PackageLayout,
    ProjectPaths,
    RuntimePaths,
    materialize_personalization,
    plan_bootstrap,
    plan_auto_check_update_setting,
    plan_configure,
    plan_enable,
    plan_personalize,
    plan_project_install,
    plan_update,
)
from runtime.markers import (
    AUTO_CHECK_UPDATE_PLACEHOLDER,
    PROJECT_LOCAL,
    PROJECT_PERSONALIZATION,
    USER_MANAGED,
    extract,
    render_project_entry,
)
from runtime.migrations import migrate_config_resource
from runtime.plan import OperationPlan, read_string_list, resolve_owned_runtime_path
from runtime.release import (
    ReleaseSelection,
    parse_semver,
    select_releases,
    summarize_release_notes,
)
from runtime.transaction import Mutation, apply


class MarkerTests(unittest.TestCase):
    def test_user_command_contract_keeps_automatic_check_optional(self) -> None:
        instructions = (PACKAGE / "user_AGENTS.md").read_text(encoding="utf-8")
        auto_check = (PACKAGE / "resources" / "auto_check_update.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("auto-check-update --json", instructions)
        self.assertEqual(instructions.count(AUTO_CHECK_UPDATE_PLACEHOLDER), 1)
        self.assertIn("auto-check-update --json", auto_check)
        self.assertIn("codex_workflow --check-update", instructions)
        self.assertIn("codex_workflow --enable_auto_check_update", instructions)
        self.assertIn("codex_workflow --disable_auto_check_update", instructions)
        self.assertIn("codex_workflow --enable_auto_update", instructions)
        self.assertIn("codex_workflow --disable_auto_update", instructions)
        self.assertIn("codex_workflow --remove", instructions)
        self.assertIn("codex_workflow --analyze-thread", instructions)

        personalization = (PACKAGE / "personalization_guide.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("resources/personalization.md", personalization)
        self.assertIn("missing or invalid", personalization)
        self.assertIn("copy that section's complete", personalization)

    def test_template_renders_independent_project_regions(self) -> None:
        template = (PACKAGE / "AGENTS.md").read_text(encoding="utf-8")
        rendered = render_project_entry(
            template,
            personalization="Personal rule.",
            local_instructions="# Existing\nKeep this.",
        )
        self.assertEqual(extract(rendered, PROJECT_PERSONALIZATION), "Personal rule.")
        self.assertEqual(extract(rendered, PROJECT_LOCAL), "# Existing\nKeep this.")

    def test_operational_policies_are_compact_and_knowledge_aware(self) -> None:
        names = ("AGENTS.md", "medium_route.md", "heavy_route.md")
        policies = {
            name: (PACKAGE / name).read_text(encoding="utf-8") for name in names
        }
        for name, text in policies.items():
            limit = 225 if name == "heavy_route.md" else 200
            self.assertLess(len(text.splitlines()), limit, name)

        heavy = policies["heavy_route.md"]
        self.assertIn("recommended approach", heavy.lower())
        self.assertIn('fork_turns="none"', heavy)
        self.assertIn("ordered execution guide", heavy.lower())
        self.assertIn("`ui-reviewer`", heavy)
        self.assertIn("rendered interaction and visual", heavy)
        self.assertIn("Never run an automatic documentation sweep, session closure, or commit", heavy)
        self.assertIn("2-4 initial workers", heavy)
        self.assertIn("Use a spawn-first sequence", heavy)
        self.assertIn("capsule owner and surface are immutable", heavy)
        self.assertIn("interrupt only when", heavy)
        self.assertIn("cumulative task budget", heavy)
        self.assertIn("Add an independent tester or reviewer only", heavy)
        self.assertIn("reuse the responsible implementer", heavy.lower())
        self.assertIn("one long native wait", heavy)
        self.assertIn("progress checkpoints", heavy)
        self.assertIn("8 substantive tool calls", heavy)
        self.assertIn("`progress_target`", heavy)
        self.assertIn("Before its first repository or task tool call", heavy)
        self.assertIn("under 60 words", heavy)
        self.assertIn("Combine checkpoints that are", heavy)
        self.assertIn("immediate push, deploy, or ship", heavy)
        self.assertIn("Assign each gate to exactly one worker", heavy)
        self.assertIn("does not rerun the implementer's fresh passing suite", heavy)

        medium = policies["medium_route.md"]
        self.assertIn("Use exactly one configured worker", medium)
        self.assertIn("Medium has no worker parallelism", medium)
        self.assertIn("route mismatch", medium)
        self.assertIn("Never create a replacement worker", medium)
        self.assertIn('fork_turns="none"', medium)
        self.assertIn("`ui-reviewer`", medium)
        self.assertIn("one long native wait", medium)
        self.assertIn("progress checkpoints", medium)
        self.assertIn("8 substantive tool", medium)
        self.assertIn("`progress_target`", medium)
        self.assertIn("Before its first repository or task tool call", medium)
        self.assertIn("under 60 words", medium)
        self.assertIn("Relay checkpoints promptly", medium)
        self.assertIn("never repeat it\nonly to obtain independent confirmation", medium)

        agents_policy = policies["AGENTS.md"]
        self.assertIn("Automatic commits, automatic session closure, and Explorer workers are forbidden", agents_policy)
        self.assertIn("repository's `AGENTS.md`", agents_policy)
        self.assertIn("regardless of task size or number of stages", agents_policy)
        self.assertIn("Consume valid worker evidence", agents_policy)
        self.assertIn("Delegation is opt-in", agents_policy)
        self.assertIn("`Luna high`", agents_policy)
        self.assertIn("always use Light", agents_policy)
        self.assertIn("Validation is milestone-based, not edit-based", agents_policy)
        self.assertIn("Never rerun an\n  unchanged command", agents_policy)
        self.assertIn("implementing worker owns focused and owner", agents_policy)
        self.assertIn("A worker capsule is immutable in owner and surface", agents_policy)
        self.assertIn("Sol stays out of the delegated read and edit surface", agents_policy)
        self.assertIn("Delegated routes remain progressively visible", agents_policy)
        self.assertIn("send_message", agents_policy)
        self.assertIn("`progress_target`", agents_policy)
        self.assertIn("no later than 8 substantive tool calls", agents_policy)
        self.assertIn("raw chain-of-thought", agents_policy)
        identity = "<role> — <task ID>"
        for policy in (agents_policy, medium, heavy):
            self.assertIn(identity, policy)
            self.assertIn("agent_id", policy)
            self.assertIn("generated person nickname", policy)
        for worker in ("scout", "implementer", "ui-implementer", "tester", "reviewer", "ui-reviewer", "doc-writer"):
            worker_text = (PACKAGE / "agents" / f"{worker}.toml").read_text(encoding="utf-8")
            self.assertIn("Require a capsule task ID", worker_text)
            self.assertIn(identity, worker_text)
            self.assertIn("agent_id", worker_text)
            self.assertIn("send_message", worker_text)
            self.assertIn("progress checkpoint", worker_text)
            self.assertIn("8 substantive tool calls", worker_text)
            self.assertIn("`progress_target`", worker_text)
            self.assertIn("Before the first repository or task tool call", worker_text)
            self.assertIn("under 60 words", worker_text)
            self.assertIn("raw chain-of-thought", worker_text)
        for documentation in (
            ROOT / "README.md",
            ROOT / "workflow_usage.md",
            PACKAGE / "configuration_guide.md",
        ):
            documentation_text = documentation.read_text(encoding="utf-8")
            self.assertIn(identity, documentation_text)
            self.assertIn("agent_id", documentation_text)

        tester = (PACKAGE / "agents" / "tester.toml").read_text(encoding="utf-8")
        executor = (PACKAGE / "agents" / "implementer.toml").read_text(
            encoding="utf-8"
        )
        ui_reviewer = (PACKAGE / "agents" / "ui-reviewer.toml").read_text(
            encoding="utf-8"
        )
        bootstrap = (PACKAGE / "bootstrap.md").read_text(encoding="utf-8")
        install = (PACKAGE / "install.md").read_text(encoding="utf-8")
        self.assertIn("minimal reproduction", tester)
        self.assertIn("Fix the owning cause", executor)
        self.assertIn("configured browser", ui_reviewer)
        self.assertIn("Do not edit files", ui_reviewer)
        self.assertIn("creates no project scaffold", bootstrap)
        self.assertIn("calls no worker", install)

    def test_reserved_marker_collision_is_rejected_during_import(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "project"
            project.mkdir()
            (project / "AGENTS.md").write_text(PROJECT_LOCAL.start, encoding="utf-8")
            with self.assertRaises(ValidationError):
                plan_bootstrap(
                    PackageLayout.resolve(PACKAGE),
                    RuntimePaths(root / "home"),
                    ProjectPaths(project),
                )

    def test_package_requires_exact_user_managed_region(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "codex_workflow"
            shutil.copytree(
                PACKAGE,
                root,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            path = root / "user_AGENTS.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(USER_MANAGED.start, "", 1), encoding="utf-8"
            )
            with self.assertRaises(ValidationError):
                PackageLayout.resolve(root)

    def test_package_requires_auto_check_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "codex_workflow"
            shutil.copytree(
                PACKAGE,
                root,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            path = root / "user_AGENTS.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    AUTO_CHECK_UPDATE_PLACEHOLDER, "", 1
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ValidationError):
                PackageLayout.resolve(root)

    def test_package_requires_auto_check_instruction_command(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "codex_workflow"
            shutil.copytree(
                PACKAGE,
                root,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            (root / "resources" / "auto_check_update.md").write_text(
                "Missing command.\n", encoding="utf-8"
            )
            with self.assertRaises(ValidationError):
                PackageLayout.resolve(root)

    def test_update_help_does_not_publish_local_source_option(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", str(PACKAGE / "workflow.py"), "update", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("--source", completed.stdout)
        self.assertNotIn("--apply", completed.stdout)

    def test_explicit_auto_check_commands_and_legacy_aliases_are_available(self) -> None:
        for command in (
            "enable-auto-check-update",
            "disable-auto-check-update",
            "enable-auto-update",
            "disable-auto-update",
            "check-update",
        ):
            completed = subprocess.run(
                [sys.executable, "-B", str(PACKAGE / "workflow.py"), command, "--help"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_configure_help_omits_handoff_context_option(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(PACKAGE / "workflow.py"),
                "configure",
                "--help",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("--handoff-context-turns", completed.stdout)
        self.assertIn("--implementation-effort", completed.stdout)
        self.assertIn("--support-effort", completed.stdout)

    def test_remove_help_hides_internal_confirmation_flag(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-B", str(PACKAGE / "workflow.py"), "remove", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("--confirm", completed.stdout)


class SafetyTests(unittest.TestCase):
    def test_owned_runtime_manifest_is_confined_and_typed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runtime_root = Path(temporary) / "runtime"
            with self.assertRaises(ValidationError):
                resolve_owned_runtime_path(runtime_root, "../../outside.txt")
            with self.assertRaises(ValidationError):
                resolve_owned_runtime_path(runtime_root, "/tmp/outside.txt")
        with self.assertRaises(ValidationError):
            read_string_list({"owned_runtime_files": None}, "owned_runtime_files")

    def test_backup_skips_missing_optional_user_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "project"
            project.mkdir()
            mutations: list[Mutation] = []
            append_backup_mutations(
                mutations,
                root / "backup",
                RuntimePaths(root / "home"),
                ProjectPaths(project),
            )
            self.assertEqual(mutations, [])


class AnalyzeTests(unittest.TestCase):
    def test_native_parent_and_direct_child_are_aggregated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            sessions = Path(temporary)
            parent_id = "01parent"
            child_id = "01child"
            parent = sessions / f"rollout-{parent_id}.jsonl"
            child = sessions / f"rollout-{child_id}.jsonl"

            def write(path: Path, records: list[dict[str, object]]) -> None:
                path.write_text(
                    "".join(json.dumps(record) + "\n" for record in records),
                    encoding="utf-8",
                )

            write(
                parent,
                [
                    {
                        "timestamp": "2026-08-18T10:00:00Z",
                        "type": "session_meta",
                        "payload": {"id": parent_id, "source": {}},
                    },
                    {
                        "timestamp": "2026-08-18T10:00:01Z",
                        "type": "turn_context",
                        "payload": {"model": "gpt-5.6-sol", "effort": "high"},
                    },
                    {
                        "timestamp": "2026-08-18T10:00:02Z",
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "name": "exec",
                            "input": "text(await tools.apply_patch(patch));",
                        },
                    },
                    {
                        "timestamp": "2026-08-18T10:00:02Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "token_count",
                            "info": {
                                "total_token_usage": {
                                    "input_tokens": 100,
                                    "cached_input_tokens": 40,
                                    "cache_write_input_tokens": 0,
                                    "output_tokens": 20,
                                    "reasoning_output_tokens": 10,
                                    "total_tokens": 120,
                                }
                            },
                        },
                    },
                ],
            )
            write(
                child,
                [
                    {
                        "timestamp": "2026-08-18T10:00:03Z",
                        "type": "session_meta",
                        "payload": {
                            "id": child_id,
                            "source": {
                                "subagent": {
                                    "thread_spawn": {
                                        "parent_thread_id": parent_id,
                                        "agent_path": "/root/task",
                                        "agent_role": "implementer",
                                    }
                                }
                            },
                        },
                    },
                    {
                        "timestamp": "2026-08-18T10:00:04Z",
                        "type": "turn_context",
                        "payload": {"model": "gpt-5.6-luna", "effort": "xhigh"},
                    },
                    {
                        "timestamp": "2026-08-18T10:00:05Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "task_started",
                            "turn_id": "turn",
                            "started_at": 1787047205,
                        },
                    },
                    {
                        "timestamp": "2026-08-18T10:00:07Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "task_complete",
                            "turn_id": "turn",
                            "completed_at": 1787047207,
                            "duration_ms": 2000,
                        },
                    },
                ],
            )

            result = analyze_thread(parent_id, sessions_root=sessions)
            self.assertEqual(result["child_count"], 1)
            self.assertEqual(result["max_child_concurrency"], 1)
            self.assertEqual(result["children"][0]["agent_role"], "implementer")
            self.assertEqual(result["parent"]["nested_tool_calls"]["apply_patch"], 1)
            self.assertEqual(
                result["totals_by_model"]["gpt-5.6-sol"]["total_tokens"], 120
            )


class ConfigTests(unittest.TestCase):
    def test_package_default_disables_automatic_update_checks(self) -> None:
        raw = json.loads(
            (PACKAGE / "resources" / "workflow_config.default.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(raw["auto_check_update"])
        self.assertEqual(raw["schema_version"], 6)
        self.assertEqual(raw["default_executor_reasoning_effort"], "xhigh")
        self.assertEqual(raw["default_subagent_reasoning_effort"], "high")
        self.assertEqual(raw["max_total_workers"], 6)
        self.assertNotIn("nickname", raw)
        self.assertNotIn("display_name", raw)
        self.assertFalse(WorkflowConfig.from_mapping(raw).auto_check_update)

    def test_newer_persistent_schema_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            migrate_config_resource(
                {"schema_version": 7},
                {"schema_version": 6},
            )

    def test_v2_config_migration_replaces_legacy_roles(self) -> None:
        migrated = migrate_config_resource(
            {
                "schema_version": 2,
                "enabled_workers": ["executor_luna", "doc-writer", "explorer"],
            },
            {"schema_version": 6},
        )
        self.assertEqual(migrated["schema_version"], 6)
        self.assertIn("implementer", migrated["enabled_workers"])
        self.assertIn("ui-reviewer", migrated["enabled_workers"])
        self.assertNotIn("end_of_session", migrated["enabled_workers"])
        self.assertNotIn("end_of_session_context_turns", migrated)

    def test_v3_config_migration_removes_handoff_context_setting(self) -> None:
        migrated = migrate_config_resource(
            {
                "schema_version": 3,
                "end_of_session_context_turns": 150,
            },
            {"schema_version": 6},
        )
        self.assertEqual(migrated["schema_version"], 6)
        self.assertNotIn("end_of_session_context_turns", migrated)

    def test_v5_config_migration_adds_budget_and_preserves_reasoning(self) -> None:
        migrated = migrate_config_resource(
            {
                "schema_version": 5,
                "default_executor_reasoning_effort": "high",
                "default_subagent_reasoning_effort": "high",
                "max_concurrent_workers": 4,
            },
            {"schema_version": 6, "max_total_workers": 6},
        )
        self.assertEqual(migrated["schema_version"], 6)
        self.assertEqual(migrated["max_total_workers"], 6)
        self.assertEqual(migrated["default_executor_reasoning_effort"], "high")
        self.assertEqual(migrated["default_subagent_reasoning_effort"], "high")

    def test_worker_limit_above_platform_limit_is_rejected(self) -> None:
        raw = json.loads(
            (PACKAGE / "resources" / "workflow_config.default.json").read_text(
                encoding="utf-8"
            )
        )
        raw["max_concurrent_workers"] = 9
        with self.assertRaises(ValidationError):
            WorkflowConfig.from_mapping(raw)

    def test_cumulative_worker_budget_is_positive_and_capped(self) -> None:
        raw = json.loads(
            (PACKAGE / "resources" / "workflow_config.default.json").read_text(
                encoding="utf-8"
            )
        )
        raw["max_total_workers"] = 0
        with self.assertRaises(ValidationError):
            WorkflowConfig.from_mapping(raw)
        raw["max_total_workers"] = 7
        with self.assertRaises(ValidationError):
            WorkflowConfig.from_mapping(raw)

    def test_toml_patch_preserves_unrelated_content(self) -> None:
        config = WorkflowConfig.from_mapping(
            json.loads(
                (PACKAGE / "resources" / "workflow_config.default.json").read_text(
                    encoding="utf-8"
                )
            )
        )
        original = 'model = "custom"\n\n[agents]\nenabled = false\nother = 7\n'
        rendered = patch_codex_config(original, config)
        self.assertIn('model = "custom"', rendered)
        self.assertIn("other = 7", rendered)
        self.assertIn("max_concurrent_threads_per_session = 4", rendered)
        self.assertIn('default_subagent_model = "gpt-5.6-luna"', rendered)
        self.assertIn("max_depth = 1", rendered)

    def test_toml_remove_preserves_unrelated_content(self) -> None:
        original = (
            'model = "custom"\n\n'
            "[agents]\n"
            "enabled = true\n"
            "default_subagent_model = \"gpt-5.6-luna\"\n"
            "default_subagent_reasoning_effort = \"xhigh\"\n"
            "max_concurrent_threads_per_session = 4\n"
            "max_depth = 1\n"
            "keep_agent = true\n"
        )
        rendered = remove_workflow_owned_config(original)
        self.assertIn('model = "custom"', rendered)
        self.assertIn("keep_agent = true", rendered)
        self.assertNotIn("max_concurrent_threads_per_session", rendered)
        self.assertNotIn("default_subagent_model", rendered)
        self.assertIn("[agents]", rendered)
        self.assertNotIn("enabled = true", rendered)

    def test_heavy_snapshot_is_rendered_from_config(self) -> None:
        config = WorkflowConfig.from_mapping(
            json.loads(
                (PACKAGE / "resources" / "workflow_config.default.json").read_text(
                    encoding="utf-8"
                )
            )
        )
        rendered = render_heavy_route(
            (PACKAGE / "heavy_route.md").read_text(encoding="utf-8"), config
        )
        self.assertIn("Maximum concurrent child workers: `4`", rendered)
        self.assertIn("Cumulative task worker budget: `6` total workers", rendered)
        self.assertIn("Default executor: `implementer` (`xhigh`", rendered)
        self.assertIn("Implementation workers: `gpt-5.6-luna` (`xhigh`", rendered)
        self.assertIn("UI workers: `gpt-5.6-terra` (`xhigh` implementation", rendered)
        self.assertIn("Support workers: `gpt-5.6-luna` (`high`", rendered)
        self.assertIn("Never run an automatic documentation sweep, session closure, or commit", rendered)

    def test_role_defaults_split_implementation_and_support_effort(self) -> None:
        expected = {
            "scout": "high",
            "implementer": "xhigh",
            "ui-implementer": "xhigh",
            "tester": "high",
            "reviewer": "high",
            "ui-reviewer": "high",
            "doc-writer": "high",
        }
        raw = json.loads(
            (PACKAGE / "resources" / "workflow_config.default.json").read_text(
                encoding="utf-8"
            )
        )
        config = WorkflowConfig.from_mapping(raw)
        expected_models = {
            "ui-implementer": "gpt-5.6-terra",
            "ui-reviewer": "gpt-5.6-terra",
        }
        for worker, effort in expected.items():
            template = (PACKAGE / "agents" / f"{worker}.toml").read_text(
                encoding="utf-8"
            )
            rendered = render_worker_template(template, worker=worker, config=config)
            self.assertIn(f'model_reasoning_effort = "{effort}"', rendered)
            self.assertEqual(rendered.count("model_reasoning_effort ="), 1)
            model = expected_models.get(worker, "gpt-5.6-luna")
            self.assertIn(f'model = "{model}"', rendered)
            self.assertEqual(rendered.count("model ="), 1)


class ReleaseTests(unittest.TestCase):
    def test_check_update_reports_new_release_notes_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "codex-home"
            runtime = home / "codex_workflow"
            runtime.mkdir(parents=True)
            (runtime / "VERSION").write_text("1.1.1\n", encoding="utf-8")
            release = ReleaseSelection(
                "1.2.0",
                parse_semver("1.2.0"),
                "codex_workflow-1.2.0.zip",
                "https://example/1.2.0.zip",
                "https://example/SHA256SUMS",
                "## Changes\n- Add release-note summaries.",
                "https://example/releases/1.2.0",
            )
            output = io.StringIO()
            argv = ["workflow.py", "check-update", "--codex-home", str(home), "--json"]
            with (
                mock.patch.object(workflow_cli, "select_releases", return_value=[release]),
                mock.patch.object(sys, "argv", argv),
                contextlib.redirect_stdout(output),
            ):
                self.assertEqual(workflow_cli.main(), 0)
            summary = json.loads(output.getvalue())
            self.assertEqual(summary["status"], "update available")
            self.assertEqual(summary["updates"][0]["version"], "1.2.0")
            self.assertIn("release-note summaries", summary["summary"])
            self.assertEqual((runtime / "VERSION").read_text(), "1.1.1\n")

    def test_select_releases_keeps_installable_versions_and_notes(self) -> None:
        records = [
            {
                "tag_name": "v1.3.0",
                "draft": False,
                "body": "## Changes\n- Add explicit update summaries.",
                "html_url": "https://github.com/example/releases/1.3.0",
                "assets": [
                    {
                        "name": "codex_workflow-1.3.0.zip",
                        "browser_download_url": "https://example/1.3.0.zip",
                    },
                    {"name": "SHA256SUMS", "browser_download_url": "https://example/sums"},
                ],
            },
            {
                "tag_name": "v1.2.0",
                "draft": False,
                "body": "- Older change",
                "assets": [
                    {
                        "name": "codex_workflow-1.2.0.zip",
                        "browser_download_url": "https://example/1.2.0.zip",
                    },
                    {"name": "SHA256SUMS", "browser_download_url": "https://example/sums"},
                ],
            },
            {"tag_name": "v1.4.0", "draft": True, "assets": []},
        ]
        with mock.patch("runtime.release._read_json_url", return_value=records):
            releases = select_releases()
        self.assertEqual([release.version_text for release in releases], ["1.3.0", "1.2.0"])
        self.assertIn("explicit update summaries", releases[0].release_notes)

    def test_release_note_summary_strips_markdown_and_limits_length(self) -> None:
        summary = summarize_release_notes(
            "## Changes\n- `check-update` now reports [notes](https://example)."
        )
        self.assertEqual(summary, "Changes check-update now reports notes.")
        self.assertEqual(
            summarize_release_notes("", max_length=10),
            "No release notes were provided.",
        )


class TransactionTests(unittest.TestCase):
    def test_failed_transaction_restores_all_targets(self) -> None:
        from runtime import transaction

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first"
            second = root / "second"
            first.write_bytes(b"old")
            original_write = transaction._atomic_write
            calls = 0

            def fail_once(path: Path, content: bytes, mode: int) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected failure")
                original_write(path, content, mode)

            with mock.patch("runtime.transaction._atomic_write", side_effect=fail_once):
                with self.assertRaises(TransactionError):
                    apply([Mutation(first, b"new"), Mutation(second, b"created")])
            self.assertEqual(first.read_bytes(), b"old")
            self.assertFalse(second.exists())


class LifecycleIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.codex_home = self.root / "codex-home"
        self.project_root = self.root / "project"
        self.project_root.mkdir()
        self.runtime = RuntimePaths(self.codex_home)
        self.project = ProjectPaths(self.project_root)
        self.package = PackageLayout.resolve(PACKAGE)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def bootstrap(self, *, existing_agents: str | None = None) -> OperationPlan:
        if existing_agents is not None:
            self.project.active.write_text(existing_agents, encoding="utf-8")
        plan = plan_bootstrap(self.package, self.runtime, self.project)
        self.assertFalse(self.codex_home.exists())
        plan.apply()
        return plan

    def incoming_package(self, directory: str, version: str | None = None) -> PackageLayout:
        version = version or PACKAGE_VERSION
        incoming_root = self.root / directory / "codex_workflow"
        shutil.copytree(
            PACKAGE,
            incoming_root,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        (incoming_root / "VERSION").write_text(f"{version}\n", encoding="utf-8")
        user_agents = (incoming_root / "user_AGENTS.md").read_text(encoding="utf-8")
        (incoming_root / "user_AGENTS.md").write_text(
            user_agents.replace(
                f"codex-workflow-version: {PACKAGE_VERSION}",
                f"codex-workflow-version: {version}",
            ),
            encoding="utf-8",
        )
        return PackageLayout.resolve(incoming_root)

    def test_bootstrap_imports_existing_agents_and_materializes_runtime(self) -> None:
        plan = self.bootstrap(
            existing_agents="# Existing instructions\nKeep local policy.\n"
        )
        entry = self.project.active.read_text(encoding="utf-8")
        self.assertEqual(
            extract(entry, PROJECT_LOCAL),
            "# Existing instructions\nKeep local policy.",
        )
        self.assertTrue((self.runtime.runtime / "workflow.py").is_file())
        self.assertTrue((self.runtime.runtime / "templates" / "AGENTS.md").is_file())
        self.assertTrue((self.runtime.agents / "implementer.toml").is_file())
        self.assertTrue((self.runtime.agents / "ui-implementer.toml").is_file())
        self.assertTrue((self.runtime.agents / "ui-reviewer.toml").is_file())
        self.assertIn(
            "max_concurrent_threads_per_session = 4",
            self.runtime.config_toml.read_text(encoding="utf-8"),
        )
        self.assertIn(
            'default_subagent_model = "gpt-5.6-luna"',
            self.runtime.config_toml.read_text(encoding="utf-8"),
        )
        self.assertIn(
            'default_subagent_reasoning_effort = "high"',
            self.runtime.config_toml.read_text(encoding="utf-8"),
        )
        self.assertIn(
            'model = "gpt-5.6-terra"',
            (self.runtime.agents / "ui-implementer.toml").read_text(encoding="utf-8"),
        )
        self.assertIn(
            'model = "gpt-5.6-terra"',
            (self.runtime.agents / "ui-reviewer.toml").read_text(encoding="utf-8"),
        )
        installed_user_agents = self.runtime.user_agents.read_text(encoding="utf-8")
        self.assertIn("Use Sol as the coordinator", installed_user_agents)
        self.assertNotIn("auto-check-update --json", installed_user_agents)
        self.assertNotIn(AUTO_CHECK_UPDATE_PLACEHOLDER, installed_user_agents)
        self.assertEqual(plan.agent_actions, [])

        repeated = plan_project_install(self.package, self.project)
        self.assertEqual(repeated.agent_actions, [])

    def test_bootstrap_cleans_project_staging_and_updates_gitignore(self) -> None:
        staging = self.project_root / "Codex_Workflow"
        (staging / "nested").mkdir(parents=True)
        (staging / "nested" / "package.txt").write_text("staged", encoding="utf-8")
        (self.project_root / ".gitignore").write_text("# local rules\n", encoding="utf-8")

        self.bootstrap()

        self.assertFalse(staging.exists())
        gitignore = (self.project_root / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("# local rules\n", gitignore)
        for entry in (".codex_workflow_hidden_resources/", "AGENTS.md"):
            self.assertEqual(gitignore.splitlines().count(entry), 1)
        self.assertNotIn("agent_docs/", gitignore)

        # A repeated project install is idempotent and does not duplicate rules.
        plan_project_install(self.package, self.project).apply()
        repeated = (self.project_root / ".gitignore").read_text(encoding="utf-8")
        for entry in (".codex_workflow_hidden_resources/", "AGENTS.md"):
            self.assertEqual(repeated.splitlines().count(entry), 1)

    def test_unactivated_workers_are_materialized_for_codex(self) -> None:
        self.bootstrap()
        for worker in self.package.worker_names:
            self.assertTrue((self.runtime.agents / f"{worker}.toml").is_file())
            self.assertTrue(
                (self.runtime.runtime / "templates" / "agents" / f"{worker}.toml").is_file()
            )
        state = json.loads((self.runtime.runtime / "install_state.json").read_text())
        self.assertEqual(set(state["owned_workers"]), self.package.worker_names)

    def test_configure_updates_luna_effort_without_touching_local_region(self) -> None:
        self.bootstrap(existing_agents="Local policy.\n")
        plan = plan_configure(
            self.runtime,
            {
                "default_executor_reasoning_effort": "high",
                "default_subagent_reasoning_effort": "high",
                "max_concurrent_workers": 7,
                "max_total_workers": 5,
            },
        )
        plan.apply()
        configured = json.loads(
            (self.runtime.runtime / "workflow_config.json").read_text(encoding="utf-8")
        )
        self.assertEqual(configured["default_executor"], "implementer")
        self.assertEqual(configured["max_concurrent_workers"], 7)
        self.assertEqual(configured["max_total_workers"], 5)
        self.assertEqual(configured["default_subagent_reasoning_effort"], "high")
        implementer = (self.runtime.agents / "implementer.toml").read_text(encoding="utf-8")
        self.assertIn('model_reasoning_effort = "high"', implementer)
        for worker in configured["enabled_workers"]:
            rendered_worker = (self.runtime.agents / f"{worker}.toml").read_text(
                encoding="utf-8"
            )
            self.assertIn('model_reasoning_effort = "high"', rendered_worker)
        self.assertEqual(extract(self.project.active.read_text(), PROJECT_LOCAL), "Local policy.")

    def test_configure_keeps_unactivated_worker_definitions_materialized(self) -> None:
        self.bootstrap()
        current = json.loads(
            (self.runtime.runtime / "workflow_config.json").read_text(encoding="utf-8")
        )
        current["enabled_workers"].remove("scout")
        plan_configure(self.runtime, {"enabled_workers": current["enabled_workers"]}).apply()
        self.assertTrue((self.runtime.agents / "scout.toml").is_file())
        state = json.loads((self.runtime.runtime / "install_state.json").read_text())
        self.assertIn("scout", state["owned_workers"])

    def test_configure_materializes_auto_check_instruction_when_changed(self) -> None:
        self.bootstrap()
        plan_configure(self.runtime, {"auto_check_update": True}).apply()
        configured = json.loads(
            (self.runtime.runtime / "workflow_config.json").read_text(encoding="utf-8")
        )
        self.assertTrue(configured["auto_check_update"])
        self.assertIn(
            "auto-check-update --json",
            self.runtime.user_agents.read_text(encoding="utf-8"),
        )

    def test_personalize_and_enable_disable_preserve_regions(self) -> None:
        self.bootstrap(existing_agents="Local policy.\n")
        customized = (PACKAGE / "resources" / "personalization.md").read_text(
            encoding="utf-8"
        ).replace(
            "Status: default\nDecision: Preserve the workflow-managed default Design Principles.",
            "Status: customized\nDecision: Prefer explicit ports and adapters.",
        )
        plan_personalize(self.project, customized).apply()
        entry = self.project.active.read_text(encoding="utf-8")
        self.assertEqual(extract(entry, PROJECT_PERSONALIZATION), "Prefer explicit ports and adapters.")
        self.assertEqual(extract(entry, PROJECT_LOCAL), "Local policy.")
        plan_enable(self.project, enable=False).apply()
        self.assertFalse(self.project.active.exists())
        self.assertTrue(self.project.disabled.exists())
        plan_enable(self.project, enable=True).apply()
        self.assertTrue(self.project.active.exists())
        self.assertFalse(self.project.disabled.exists())

        self.project.personalization.unlink()
        defaults = (PACKAGE / "resources" / "personalization.md").read_text(
            encoding="utf-8"
        )
        plan_personalize(self.project, defaults).apply()
        self.assertEqual(self.project.personalization.read_text(encoding="utf-8"), defaults)
        self.assertEqual(
            extract(self.project.active.read_text(encoding="utf-8"), PROJECT_PERSONALIZATION),
            "",
        )

    def test_install_rejects_personalization_resource_drift(self) -> None:
        self.bootstrap()
        resource = self.project.personalization.read_text(encoding="utf-8")
        self.project.personalization.write_text(
            resource.replace(
                "Status: default\nDecision: Preserve the workflow-managed default Design Principles.",
                "Status: customized\nDecision: Prefer explicit ports and adapters.",
            ),
            encoding="utf-8",
        )
        with self.assertRaises(ValidationError):
            plan_project_install(self.package, self.project)

    def test_update_preserves_configuration_managed_and_local_content(self) -> None:
        self.bootstrap(existing_agents="Local policy.\n")
        plan_configure(
            self.runtime,
            {
                "default_executor_reasoning_effort": "high",
                "default_subagent_reasoning_effort": "high",
                "max_concurrent_workers": 7,
            },
        ).apply()
        plan_auto_check_update_setting(self.runtime, enabled=True).apply()
        self.assertIn(
            "auto-check-update --json",
            self.runtime.user_agents.read_text(encoding="utf-8"),
        )
        installed_config_path = self.runtime.runtime / "workflow_config.json"
        (self.runtime.agents / "implementer.toml").write_text(
            "# local worker override\n", encoding="utf-8"
        )
        incoming_root = self.root / "incoming" / "codex_workflow"
        shutil.copytree(PACKAGE, incoming_root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (incoming_root / "VERSION").write_text("2.4.0\n", encoding="utf-8")
        user_agents = (incoming_root / "user_AGENTS.md").read_text(encoding="utf-8")
        (incoming_root / "user_AGENTS.md").write_text(
            user_agents.replace(
                f"codex-workflow-version: {PACKAGE_VERSION}",
                "codex-workflow-version: 2.4.0",
            ),
            encoding="utf-8",
        )
        incoming = PackageLayout.resolve(incoming_root)
        plan_update(incoming, self.runtime, self.project).apply()
        entry = self.project.active.read_text(encoding="utf-8")
        self.assertEqual(extract(entry, PROJECT_LOCAL), "Local policy.")
        self.assertEqual((self.runtime.runtime / "VERSION").read_text(), "2.4.0\n")
        updated_config = json.loads(installed_config_path.read_text(encoding="utf-8"))
        self.assertEqual(updated_config["default_executor"], "implementer")
        self.assertEqual(updated_config["max_concurrent_workers"], 7)
        self.assertEqual(updated_config["default_executor_reasoning_effort"], "high")
        self.assertTrue(updated_config["auto_check_update"])
        self.assertIn(
            "auto-check-update --json",
            self.runtime.user_agents.read_text(encoding="utf-8"),
        )
        self.assertNotIn(
            "local worker override",
            (self.runtime.agents / "implementer.toml").read_text(encoding="utf-8"),
        )
        self.assertTrue(any((self.runtime.runtime / ".backups").iterdir()))

    def test_projects_update_against_their_recorded_historical_sources(self) -> None:
        self.bootstrap()
        second_root = self.root / "second-project"
        second_root.mkdir()
        second = ProjectPaths(second_root)
        plan_project_install(self.package, second).apply()

        incoming = self.incoming_package("multi-project-incoming", "2.4.0")
        incoming_template = incoming.project_template.read_text(encoding="utf-8")
        incoming.project_template.write_text(
            incoming_template.replace("## Core policy", "## Core policy (2.1)"),
            encoding="utf-8",
        )
        incoming = PackageLayout.resolve(incoming.root)

        plan_update(incoming, self.runtime, self.project).apply()
        second_plan = plan_update(incoming, self.runtime, second)
        self.assertEqual(second_plan.details["from_version"], "2.4.0")
        self.assertEqual(second_plan.details["project_from_version"], PACKAGE_VERSION)
        second_plan.apply()
        self.assertIn(
            "## Core policy (2.1)", second.active.read_text(encoding="utf-8")
        )

    def test_update_applies_config_migration_without_resetting_user_values(self) -> None:
        self.bootstrap()
        config_path = self.runtime.runtime / "workflow_config.json"
        configured = json.loads(config_path.read_text(encoding="utf-8"))
        configured["schema_version"] = 4
        configured["default_executor_reasoning_effort"] = "max"
        configured["max_concurrent_workers"] = 8
        configured["max_executor_sol_instances"] = 1
        configured.pop("default_subagent_model")
        configured.pop("default_subagent_reasoning_effort")
        config_path.write_text(json.dumps(configured) + "\n", encoding="utf-8")

        incoming = self.incoming_package("config-migration-incoming", "2.4.0")
        plan_update(incoming, self.runtime, self.project).apply()
        migrated = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["schema_version"], 6)
        self.assertEqual(migrated["default_executor_reasoning_effort"], "xhigh")
        self.assertEqual(migrated["default_subagent_reasoning_effort"], "xhigh")
        self.assertEqual(migrated["max_total_workers"], 6)
        self.assertEqual(migrated["max_concurrent_workers"], 8)
        self.assertNotIn("max_executor_sol_instances", migrated)

    def test_cli_install_reports_global_state_without_inspecting_project(self) -> None:
        self.bootstrap()
        command = [
            sys.executable,
            "-B",
            str(self.runtime.runtime / "workflow.py"),
            "install",
            "--codex-home",
            str(self.codex_home),
            "--project",
            str(self.project_root),
            "--json",
        ]
        enabled = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(enabled.returncode, 0, enabled.stderr)
        self.assertEqual(json.loads(enabled.stdout)["status"], "globally enabled")
        self.assertEqual(
            json.loads(enabled.stdout)["instruction"],
            "No per-project installation is required.",
        )

        plan_enable(self.project, enable=False).apply()
        disabled = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(disabled.returncode, 0, disabled.stderr)
        self.assertEqual(json.loads(disabled.stdout)["status"], "globally enabled")

        plan_enable(self.project, enable=True).apply()
        text = self.project.active.read_text(encoding="utf-8")
        self.project.active.write_text(
            text.replace("## Core policy", "## Locally Changed Core Policy"),
            encoding="utf-8",
        )
        stale = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(stale.returncode, 0, stale.stderr)
        self.assertEqual(json.loads(stale.stdout)["status"], "globally enabled")

    def test_update_preserves_disabled_project_state(self) -> None:
        self.bootstrap()
        plan_enable(self.project, enable=False).apply()
        plan_update(
            self.incoming_package("disabled-incoming"),
            self.runtime,
            self.project,
        ).apply()
        self.assertFalse(self.project.active.exists())
        self.assertTrue(self.project.disabled.exists())
        state = json.loads(self.project.state.read_text(encoding="utf-8"))
        self.assertFalse(state["enabled"])

    def test_cli_install_requires_global_bootstrap_and_leaves_project_untouched(self) -> None:
        project_root = self.root / "cli-project"
        project_root.mkdir()
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(PACKAGE / "workflow.py"),
                "install",
                "--package-root",
                str(PACKAGE),
                "--codex-home",
                str(self.codex_home),
                "--project",
                str(project_root),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 1, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertIn("global bootstrap is not installed", summary["error"])
        self.assertFalse((project_root / "AGENTS.md").exists())

    def test_cli_bootstrap_installs_globally_without_touching_project(self) -> None:
        project_root = self.root / "bootstrap-project"
        project_root.mkdir()
        project_agents = project_root / "AGENTS.md"
        project_agents.write_text("# Project policy\n", encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(PACKAGE / "workflow.py"),
                "bootstrap",
                "--package-root",
                str(PACKAGE),
                "--codex-home",
                str(self.codex_home),
                "--project",
                str(project_root),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["applied"])
        self.assertEqual(project_agents.read_text(encoding="utf-8"), "# Project policy\n")
        self.assertFalse((project_root / ".codex_workflow_hidden_resources").exists())
        self.assertIn(
            "Use Sol as the coordinator",
            self.runtime.user_agents.read_text(encoding="utf-8"),
        )

    def test_remove_requires_second_confirmation_and_cleans_owned_files(self) -> None:
        self.bootstrap(existing_agents="Local policy.\n")
        self.project.docs.mkdir()
        (self.project.docs / "project_overview.md").write_text(
            "User-owned documentation.\n", encoding="utf-8"
        )
        user_agents = self.runtime.user_agents.read_text(encoding="utf-8")
        self.runtime.user_agents.write_text(
            "# Keep this user policy.\n\n" + user_agents,
            encoding="utf-8",
        )
        config = self.runtime.config_toml.read_text(encoding="utf-8")
        config = config.replace(
            "[agents]\nenabled = true",
            "[agents]\nenabled = true\nkeep_agent = true",
        )
        config += '\n[features.multi_agent_v2]\nkeep_feature = "keep"\n'
        self.runtime.config_toml.write_text(
            'model = "keep"\n\n' + config,
            encoding="utf-8",
        )
        unrelated_worker = self.runtime.agents / "unrelated.toml"
        unrelated_worker.write_text('model = "keep"\n', encoding="utf-8")

        command = [
            sys.executable,
            "-B",
            str(self.runtime.runtime / "workflow.py"),
            "remove",
            "--codex-home",
            str(self.codex_home),
            "--project",
            str(self.project_root),
            "--json",
        ]
        planned = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(planned.returncode, 0, planned.stderr)
        planned_summary = json.loads(planned.stdout)
        self.assertFalse(planned_summary["applied"])
        self.assertTrue(planned_summary["confirmation_required"])
        self.assertTrue(self.project.active.is_file())
        self.assertTrue(self.runtime.runtime.is_dir())

        confirmed = subprocess.run(
            [*command[:-1], "--confirm", "--json"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(confirmed.returncode, 0, confirmed.stderr)
        self.assertTrue(json.loads(confirmed.stdout)["applied"])
        self.assertTrue(self.project.active.exists())
        self.assertTrue(self.project.hidden_dir.exists())
        self.assertTrue((self.project.docs / "project_overview.md").is_file())
        self.assertFalse(self.runtime.runtime.exists())
        self.assertTrue(unrelated_worker.is_file())
        self.assertEqual(
            self.runtime.user_agents.read_text(encoding="utf-8"),
            "# Keep this user policy.\n",
        )
        remaining_config = self.runtime.config_toml.read_text(encoding="utf-8")
        self.assertIn('model = "keep"', remaining_config)
        self.assertIn("keep_agent = true", remaining_config)
        self.assertIn('keep_feature = "keep"', remaining_config)
        self.assertNotIn("max_concurrent_threads_per_session", remaining_config)

    def test_update_allows_missing_optional_codex_config(self) -> None:
        self.bootstrap()
        self.runtime.config_toml.unlink()
        plan = plan_update(
            self.incoming_package("missing-config-incoming"),
            self.runtime,
            self.project,
        )
        self.assertEqual(plan.operation, "update")

    def test_update_rejects_unsafe_owned_runtime_state(self) -> None:
        self.bootstrap()
        outside = self.root / "outside.txt"
        outside.write_text("keep", encoding="utf-8")
        state_path = self.runtime.runtime / "install_state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["owned_runtime_files"] = ["../../outside.txt"]
        state_path.write_text(json.dumps(state) + "\n", encoding="utf-8")
        with self.assertRaises(ValidationError):
            plan_update(
                self.incoming_package("unsafe-state-incoming"),
                self.runtime,
                self.project,
            )
        self.assertTrue(outside.is_file())

    def test_disable_auto_check_is_scoped_and_skips_network_check(self) -> None:
        self.bootstrap()
        default_user_agents = self.runtime.user_agents.read_text(encoding="utf-8")
        self.assertNotIn("auto-check-update --json", default_user_agents)
        self.runtime.user_agents.write_text(
            default_user_agents + "\nUser-level custom instruction.\n",
            encoding="utf-8",
        )
        plan = plan_auto_check_update_setting(self.runtime, enabled=False)
        self.assertEqual(len(plan.mutations), 2)
        plan.apply()
        configured = json.loads(
            (self.runtime.runtime / "workflow_config.json").read_text(encoding="utf-8")
        )
        self.assertFalse(configured["auto_check_update"])
        self.assertNotIn(
            "auto-check-update --json",
            self.runtime.user_agents.read_text(encoding="utf-8"),
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(self.runtime.runtime / "workflow.py"),
                "auto-check-update",
                "--codex-home",
                str(self.codex_home),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "disabled")

        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(self.runtime.runtime / "workflow.py"),
                "enable-auto-check-update",
                "--codex-home",
                str(self.codex_home),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(
            json.loads(
                (self.runtime.runtime / "workflow_config.json").read_text(
                    encoding="utf-8"
                )
            )["auto_check_update"]
        )
        enabled_user_agents = self.runtime.user_agents.read_text(encoding="utf-8")
        self.assertIn("auto-check-update --json", enabled_user_agents)
        self.assertIn("User-level custom instruction.", enabled_user_agents)
        self.assertNotIn(AUTO_CHECK_UPDATE_PLACEHOLDER, enabled_user_agents)

        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(self.runtime.runtime / "workflow.py"),
                "disable-auto-check-update",
                "--codex-home",
                str(self.codex_home),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse(
            json.loads(
                (self.runtime.runtime / "workflow_config.json").read_text(
                    encoding="utf-8"
                )
            )["auto_check_update"]
        )
        disabled_user_agents = self.runtime.user_agents.read_text(encoding="utf-8")
        self.assertNotIn("auto-check-update --json", disabled_user_agents)
        self.assertIn("User-level custom instruction.", disabled_user_agents)

    def test_legacy_entry_with_edits_requires_reviewed_local_instructions(self) -> None:
        self.bootstrap()
        installed_template_path = self.runtime.runtime / "templates" / "AGENTS.md"
        legacy_template = installed_template_path.read_text(encoding="utf-8")
        legacy_template = legacy_template.replace(
            "<!-- codex-workflow-managed-start -->\n", ""
        ).replace("<!-- codex-workflow-managed-end -->\n\n", "")
        legacy_template = legacy_template.replace(
            "\n<!-- codex-workflow-project-local-instructions-start -->\n"
            "<!-- codex-workflow-project-local-instructions-end -->\n",
            "\n",
        )
        installed_template_path.write_text(legacy_template, encoding="utf-8")
        self.project.active.write_text(
            legacy_template + "\nLocal legacy addition.\n", encoding="utf-8"
        )
        incoming = self.incoming_package("legacy-incoming")
        with self.assertRaises(ValidationError):
            plan_update(incoming, self.runtime, self.project)
        plan_update(
            incoming,
            self.runtime,
            self.project,
            legacy_local_instructions="Local legacy addition.",
        ).apply()
        self.assertEqual(
            extract(self.project.active.read_text(encoding="utf-8"), PROJECT_LOCAL),
            "Local legacy addition.",
        )

    def test_update_rejects_drift_in_workflow_managed_region(self) -> None:
        self.bootstrap()
        entry = self.project.active.read_text(encoding="utf-8")
        self.project.active.write_text(
            entry.replace("## Core policy", "## Locally Changed Core Policy"),
            encoding="utf-8",
        )
        incoming = self.incoming_package("drift-incoming")
        with self.assertRaises(ValidationError):
            plan_update(incoming, self.runtime, self.project)

    def test_installed_launcher_delegates_to_incoming_update_runtime(self) -> None:
        self.bootstrap()
        incoming_root = self.root / "delegated-incoming" / "codex_workflow"
        shutil.copytree(
            PACKAGE,
            incoming_root,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        (incoming_root / "VERSION").write_text("2.4.0\n", encoding="utf-8")
        user_agents = (incoming_root / "user_AGENTS.md").read_text(encoding="utf-8")
        (incoming_root / "user_AGENTS.md").write_text(
            user_agents.replace(
                f"codex-workflow-version: {PACKAGE_VERSION}",
                "codex-workflow-version: 2.4.0",
            ),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(self.runtime.runtime / "workflow.py"),
                "update",
                "--source",
                str(incoming_root),
                "--codex-home",
                str(self.codex_home),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["details"]["to_version"], "2.4.0")
        self.assertTrue(summary["applied"])
        project_state = json.loads(self.project.state.read_text(encoding="utf-8"))
        self.assertEqual(project_state["workflow_version"], PACKAGE_VERSION)

    def test_incoming_update_ignores_unowned_project_from_older_launcher(self) -> None:
        self.bootstrap()
        ordinary_root = self.root / "ordinary-project"
        ordinary_root.mkdir()
        ordinary_agents = ordinary_root / "AGENTS.md"
        ordinary_agents.write_text("# Ordinary repository policy\n", encoding="utf-8")
        incoming = self.incoming_package("legacy-delegated-incoming", "2.4.0")

        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(incoming.root / "workflow.py"),
                "update",
                "--source",
                str(incoming.root),
                "--codex-home",
                str(self.codex_home),
                "--project",
                str(ordinary_root),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertTrue(summary["applied"])
        self.assertIn("older launcher", summary["warnings"][0])
        self.assertEqual(ordinary_agents.read_text(), "# Ordinary repository policy\n")
        self.assertEqual((self.runtime.runtime / "VERSION").read_text(), "2.4.0\n")


class PersonalizationTests(unittest.TestCase):
    def test_only_customized_decisions_are_materialized(self) -> None:
        text = (PACKAGE / "resources" / "personalization.md").read_text(encoding="utf-8")
        self.assertEqual(materialize_personalization(text), "")
        customized = text.replace(
            "Status: default\nDecision: No additional frontend profile.",
            "Status: customized\nDecision: Use the frontend profile.",
        )
        self.assertEqual(materialize_personalization(customized), "Use the frontend profile.")


if __name__ == "__main__":
    unittest.main()
