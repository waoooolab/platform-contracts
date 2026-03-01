#!/usr/bin/env python3
"""Enforce contract changelog policy when schema files are changed."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CONTRACT-CHANGELOG.md"
POLICY = ROOT / "CONTRACT-CHANGELOG-POLICY.md"


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _diff_range() -> str | None:
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        remote_ref = f"origin/{base_ref}"
        _run_git(["fetch", "--no-tags", "--depth", "1", "origin", base_ref])
        return f"{remote_ref}...HEAD"

    if _run_git(["rev-parse", "--verify", "HEAD~1"]).returncode == 0:
        return "HEAD~1...HEAD"
    return None


def _changed_files() -> list[str]:
    diff_range = _diff_range()
    if diff_range is None:
        return []
    result = _run_git(["diff", "--name-only", diff_range])
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _validate_changelog_structure() -> list[str]:
    errors: list[str] = []
    if not POLICY.exists():
        errors.append("missing CONTRACT-CHANGELOG-POLICY.md")
    if not CHANGELOG.exists():
        errors.append("missing CONTRACT-CHANGELOG.md")
        return errors

    body = CHANGELOG.read_text(encoding="utf-8")
    required_headers = (
        "# Contract Changelog",
        "## Unreleased",
        "## History",
    )
    for header in required_headers:
        if header not in body:
            errors.append(f"CONTRACT-CHANGELOG.md missing header: {header}")
    return errors


def main() -> int:
    errors = _validate_changelog_structure()
    changed = _changed_files()

    schema_changed = any(
        path.startswith("jsonschema/") and path.endswith(".json")
        for path in changed
    )
    changelog_touched = "CONTRACT-CHANGELOG.md" in changed

    if schema_changed and not changelog_touched:
        errors.append(
            "schema files changed but CONTRACT-CHANGELOG.md was not updated "
            f"(changed files: {', '.join(changed)})"
        )

    if errors:
        print("Changelog policy check FAILED:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Changelog policy check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
