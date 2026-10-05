from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn, TypeGuard

REQUIRED_DIRECTORIES = (
    ".github",
    "packages",
    "plugins",
    "docs",
    "examples",
    "scripts",
    "tests",
)
REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    ".github/copilot-instructions.md",
    ".github/bos-universal-config.json",
    ".github/workflows/lab-validation.yml",
    ".github/workflows/security.yml",
    ".github/workflows/bos-universal-gatekeeper-kicker.yml",
    "docs/repository-baseline.md",
)
PLUGIN_FILES = ("README.md", "CHANGELOG.md", "SECURITY.md", "LICENSE")
PUBLISH_STAGES = ("docker", "balena", "github_release", "companion_docker", "cloudflare_pages")
SECURITY_GATES = (
    "enable_lint",
    "enable_dependency_review",
    "enable_code_scan",
    "enable_pinned_actions_check",
    "enable_pr_title_check",
    "enable_readme_header_check",
    "enable_python_lint",
)
PLUGIN_NAME = re.compile(r"os-blackoutsecure-[a-z0-9]+(?:-[a-z0-9]+)*")


def _is_json_object(value: object) -> TypeGuard[dict[str, object]]:
    """JSON object keys are strings by construction."""
    return isinstance(value, dict)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> NoReturn:
    raise ValueError(f"Nonstandard JSON constant: {value}")


def _file_errors(root: Path, relative: str) -> list[str]:
    path = root / relative
    if any(parent.is_symlink() for parent in (path, *path.parents) if parent != root):
        return [f"{relative!r}: required files and their parents must not be symlinks"]
    if not path.is_file():
        return [f"{relative!r}: required file is missing"]
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{relative!r}: cannot read UTF-8 file: {exc}"]
    if not content.strip():
        return [f"{relative!r}: required file is empty"]
    return []


def _policy_errors(path: Path) -> list[str]:
    try:
        payload: object = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"Repository policy cannot be loaded: {exc}"]
    if not _is_json_object(payload):
        return ["Repository policy must be a JSON object"]

    errors: list[str] = []
    launchpad = payload.get("launchpad")
    if not _is_json_object(launchpad):
        errors.append("launchpad must be a JSON object")
    else:
        stages = launchpad.get("stages")
        if not _is_json_object(stages):
            errors.append("launchpad.stages must be a JSON object")
        else:
            for stage in PUBLISH_STAGES:
                if stages.get(stage) is not False:
                    errors.append(
                        f"Baseline publication guard: launchpad.stages.{stage} must be false"
                    )

        scan = launchpad.get("security_scan")
        if not _is_json_object(scan):
            errors.append("launchpad.security_scan must be a JSON object")
        else:
            if scan.get("enable") is not True or scan.get("blocks_release") is not True:
                errors.append("Launchpad security scanning must be enabled and block releases")
            if scan.get("fail_on") != "fail":
                errors.append("launchpad.security_scan.fail_on must remain fail")

    gate = payload.get("gate")
    if not _is_json_object(gate):
        errors.append("gate must be a JSON object")
    else:
        for name in SECURITY_GATES:
            if gate.get(name) is not True:
                errors.append(f"gate.{name} must remain true")
        if gate.get("code_scan_fail_on") != "fail":
            errors.append("gate.code_scan_fail_on must remain fail")
    return errors


def _plugin_errors(root: Path) -> list[str]:
    directory = root / "plugins"
    if not directory.is_dir() or directory.is_symlink():
        return []
    try:
        entries = sorted(directory.iterdir(), key=lambda entry: entry.name)
    except OSError as exc:
        return [f"Cannot enumerate plugin directories: {exc}"]

    errors: list[str] = []
    for entry in entries:
        if entry.is_symlink():
            errors.append(f"Plugin entry {entry.name!r} must not be a symlink")
        elif entry.is_dir():
            if not PLUGIN_NAME.fullmatch(entry.name):
                errors.append(f"Plugin directory {entry.name!r} must use os-blackoutsecure-<name>")
                continue
            for filename in PLUGIN_FILES:
                errors.extend(_file_errors(root, f"plugins/{entry.name}/{filename}"))
    return errors


def validate_repository(root: Path) -> list[str]:
    if root.is_symlink():
        return ["Repository root must not be a symlink"]
    if not root.is_dir():
        return [f"Repository root does not exist: {root}"]

    errors: list[str] = []
    for relative in REQUIRED_DIRECTORIES:
        directory = root / relative
        if not directory.is_dir() or directory.is_symlink():
            errors.append(f"{relative!r}: required directory is missing or is a symlink")
    for relative in REQUIRED_FILES:
        errors.extend(_file_errors(root, relative))
    errors.extend(_plugin_errors(root))

    policy = ".github/bos-universal-config.json"
    if not _file_errors(root, policy):
        errors.extend(_policy_errors(root / policy))
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate offline OPNsense lab repository contracts."
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Repository contracts: PASS")
    print("FreeBSD builds, signing, and OPNsense runtime: Not Assessed")
    print("Cloudflare publication: Not Assessed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
