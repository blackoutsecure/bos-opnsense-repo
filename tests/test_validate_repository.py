from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_repository import (
    PLUGIN_FILES,
    POLICY_FILE,
    PUBLISH_STAGES,
    REQUIRED_DIRECTORIES,
    REQUIRED_FILES,
    SECURITY_GATES,
    main,
    validate_repository,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def create_fixture(root: Path) -> None:
    for relative in REQUIRED_DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)
    for relative in REQUIRED_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Fixture documentation\n", encoding="utf-8")
    stages = {stage: False for stage in PUBLISH_STAGES}
    gate: dict[str, object] = {name: True for name in SECURITY_GATES}
    gate["code_scan_fail_on"] = "fail"
    policy: dict[str, object] = {
        "launchpad": {
            "stages": stages,
            "security_scan": {"enable": True, "blocks_release": True, "fail_on": "fail"},
        },
        "gate": gate,
    }
    (root / POLICY_FILE).write_text(json.dumps(policy), encoding="utf-8")


def create_plugin(root: Path, name: str = "os-blackoutsecure-fixture") -> Path:
    directory = root / "plugins" / name
    directory.mkdir()
    for filename in PLUGIN_FILES:
        (directory / filename).write_text("Fixture plugin documentation\n", encoding="utf-8")
    return directory


class RepositoryContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        create_fixture(self.root)
        self.policy = self.root / POLICY_FILE

    def test_actual_repository(self) -> None:
        self.assertEqual(validate_repository(REPOSITORY_ROOT), [])

    def test_pr_title_types_are_individual_multiline_entries(self) -> None:
        policy = json.loads((REPOSITORY_ROOT / POLICY_FILE).read_text(encoding="utf-8"))
        self.assertEqual(
            policy["gate"]["pr_title_types"].splitlines(),
            [
                "feat",
                "fix",
                "docs",
                "style",
                "refactor",
                "perf",
                "test",
                "build",
                "ci",
                "chore",
                "revert",
            ],
        )

    def test_valid_fixture(self) -> None:
        create_plugin(self.root)
        self.assertEqual(validate_repository(self.root), [])

    def test_copilot_instructions_are_optional(self) -> None:
        instructions = self.root / ".github" / "copilot-instructions.md"
        instructions.write_text("Read AGENTS.md for repository policy.\n", encoding="utf-8")
        self.assertEqual(validate_repository(self.root), [])
        instructions.unlink()
        self.assertEqual(validate_repository(self.root), [])

    def test_canonical_agent_instructions_remain_required(self) -> None:
        (self.root / "AGENTS.md").unlink()
        self.assertIn("'AGENTS.md': required file is missing", validate_repository(self.root))

    def test_repository_policy_is_read_once(self) -> None:
        with patch.object(Path, "read_text", autospec=True, side_effect=Path.read_text) as read:
            self.assertEqual(validate_repository(self.root), [])
        self.assertEqual(sum(call.args[0] == self.policy for call in read.call_args_list), 1)

    def test_missing_required_directory(self) -> None:
        (self.root / "packages").rmdir()
        self.assertTrue(any("packages" in error for error in validate_repository(self.root)))

    def test_missing_plugin_document(self) -> None:
        plugin = create_plugin(self.root)
        (plugin / "SECURITY.md").unlink()
        self.assertTrue(any("SECURITY.md" in error for error in validate_repository(self.root)))

    def test_empty_plugin_document(self) -> None:
        plugin = create_plugin(self.root)
        (plugin / "README.md").write_text(" \n", encoding="utf-8")
        self.assertTrue(any("empty" in error for error in validate_repository(self.root)))

    def test_invalid_plugin_name(self) -> None:
        create_plugin(self.root, "invalid-plugin")
        self.assertTrue(
            any("os-blackoutsecure-" in error for error in validate_repository(self.root))
        )

    def test_plugin_directory_symlink_is_rejected(self) -> None:
        self.assert_symlink_is_rejected(create_plugin(self.root))

    def test_plugin_document_symlink_is_rejected(self) -> None:
        plugin = create_plugin(self.root)
        self.assert_symlink_is_rejected(plugin / "README.md")

    def test_repository_root_symlink_is_rejected(self) -> None:
        self.assert_symlink_is_rejected(self.root)

    def test_required_document_parent_symlink_is_rejected(self) -> None:
        self.assert_symlink_is_rejected(self.root / "docs")

    def test_policy_directory_symlink_is_rejected(self) -> None:
        self.assert_symlink_is_rejected(self.root / ".github")

    def test_symlink_above_repository_root_is_allowed(self) -> None:
        def is_symlink(path: Path) -> bool:
            return path == self.root.parent

        with patch.object(
            Path,
            "is_symlink",
            autospec=True,
            side_effect=is_symlink,
        ):
            self.assertEqual(validate_repository(self.root), [])

    def assert_symlink_is_rejected(self, link: Path) -> None:
        def is_symlink(path: Path) -> bool:
            return path == link

        with patch.object(Path, "is_symlink", autospec=True, side_effect=is_symlink):
            self.assertTrue(any("symlink" in error for error in validate_repository(self.root)))

    def test_malformed_json(self) -> None:
        self.policy.write_text("{", encoding="utf-8")
        self.assertTrue(
            any("cannot be loaded" in error for error in validate_repository(self.root))
        )

    def test_invalid_utf8_policy_is_rejected(self) -> None:
        self.policy.write_bytes(b"\xff")
        self.assertTrue(
            any("cannot read UTF-8 file" in error for error in validate_repository(self.root))
        )

    def test_unreadable_required_files_are_reported(self) -> None:
        with patch.object(Path, "read_text", side_effect=PermissionError("permission denied")):
            errors = validate_repository(self.root)
        self.assertTrue(
            any("cannot read UTF-8 file: permission denied" in error for error in errors)
        )

    def test_duplicate_json_keys(self) -> None:
        self.policy.write_text('{"launchpad": {}, "launchpad": {}}', encoding="utf-8")
        self.assertTrue(
            any("Duplicate JSON key" in error for error in validate_repository(self.root))
        )

    def test_nonstandard_json_constants_are_rejected(self) -> None:
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                create_fixture(self.root)
                content = self.policy.read_text(encoding="utf-8").replace(
                    '"blocks_release": true', f'"blocks_release": {constant}'
                )
                self.policy.write_text(content, encoding="utf-8")
                self.assertTrue(
                    any(
                        "Nonstandard JSON constant" in error
                        for error in validate_repository(self.root)
                    )
                )

    def test_policy_must_be_object(self) -> None:
        for content in ("null", "[]", '"invalid"'):
            with self.subTest(content=content):
                self.policy.write_text(content, encoding="utf-8")
                self.assertTrue(
                    any("JSON object" in error for error in validate_repository(self.root))
                )

    def test_publishing_guard_fails_closed(self) -> None:
        for stage in PUBLISH_STAGES:
            for value in ("true", '"false"', "null", "0"):
                with self.subTest(stage=stage, value=value):
                    create_fixture(self.root)
                    content = self.policy.read_text(encoding="utf-8").replace(
                        f'"{stage}": false', f'"{stage}": {value}'
                    )
                    self.policy.write_text(content, encoding="utf-8")
                    errors = validate_repository(self.root)
                    self.assertTrue(
                        any(f"stages.{stage} must be false" in error for error in errors)
                    )

    def test_missing_publication_stage_fails_closed(self) -> None:
        for stage in PUBLISH_STAGES:
            with self.subTest(stage=stage):
                create_fixture(self.root)
                policy = json.loads(self.policy.read_text(encoding="utf-8"))
                del policy["launchpad"]["stages"][stage]
                self.policy.write_text(json.dumps(policy), encoding="utf-8")
                self.assertTrue(
                    any(f"stages.{stage}" in error for error in validate_repository(self.root))
                )

    def test_security_gate_cannot_be_disabled(self) -> None:
        for name in SECURITY_GATES:
            for value in ("false", '"true"', "null", "1"):
                with self.subTest(name=name, value=value):
                    create_fixture(self.root)
                    content = self.policy.read_text(encoding="utf-8").replace(
                        f'"{name}": true', f'"{name}": {value}'
                    )
                    self.policy.write_text(content, encoding="utf-8")
                    self.assertTrue(
                        any(
                            f"{name} must remain true" in error
                            for error in validate_repository(self.root)
                        )
                    )

    def test_security_scan_cannot_be_nonblocking(self) -> None:
        content = self.policy.read_text(encoding="utf-8").replace(
            '"blocks_release": true', '"blocks_release": false'
        )
        self.policy.write_text(content, encoding="utf-8")
        self.assertTrue(any("block releases" in error for error in validate_repository(self.root)))

    def test_security_severity_cannot_be_lowered(self) -> None:
        content = self.policy.read_text(encoding="utf-8").replace(
            '"fail_on": "fail"', '"fail_on": "never"'
        )
        self.policy.write_text(content, encoding="utf-8")
        self.assertTrue(
            any("must remain fail" in error for error in validate_repository(self.root))
        )

    def test_success_reports_native_work_as_not_assessed(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--root", str(self.root)]), 0)
        self.assertIn("Repository contracts: PASS", output.getvalue())
        self.assertIn("OPNsense runtime: Not Assessed", output.getvalue())
        self.assertIn("Cloudflare publication: Not Assessed", output.getvalue())

    def test_failure_reports_errors_and_returns_nonzero(self) -> None:
        self.policy.write_text("{", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            self.assertEqual(main(["--root", str(self.root)]), 1)
        self.assertIn("ERROR:", output.getvalue())


if __name__ == "__main__":
    unittest.main()
