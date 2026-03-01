#!/usr/bin/env python3
"""Validate platform JSON schemas and version conventions."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

VERSIONED_SCHEMA_RE = re.compile(r"^(?P<stem>.+)\.v(?P<major>[1-9]\d*)\.json$")


def _jsonschema_root() -> Path:
    return Path(__file__).resolve().parents[1] / "jsonschema"


def _schema_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.json") if path.is_file())


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> int:
    root = _jsonschema_root()
    files = _schema_files(root)

    if not files:
        print("ERROR: no schema files found under jsonschema/")
        return 1

    failures: list[str] = []
    ids_seen: dict[str, Path] = {}
    versions_by_contract: dict[str, list[int]] = defaultdict(list)

    for path in files:
        rel = path.relative_to(root).as_posix()
        match = VERSIONED_SCHEMA_RE.match(path.name)
        if not match:
            failures.append(
                f"{rel}: schema filename must match <name>.v<major>.json"
            )
            continue

        versionless = f"{path.parent.relative_to(root).as_posix()}/{match.group('stem')}"
        versions_by_contract[versionless].append(int(match.group("major")))

        try:
            schema = _load_json(path)
        except json.JSONDecodeError as exc:
            failures.append(f"{rel}: invalid json ({exc})")
            continue

        if not isinstance(schema, dict):
            failures.append(f"{rel}: root must be JSON object schema")
            continue

        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            failures.append(f"{rel}: missing non-empty $id")
        else:
            existing = ids_seen.get(schema_id)
            if existing is not None:
                failures.append(
                    f"{rel}: duplicated $id already used by {existing.relative_to(root).as_posix()}"
                )
            ids_seen[schema_id] = path
            if not schema_id.endswith(rel):
                failures.append(
                    f"{rel}: $id should end with relative schema path '{rel}'"
                )

        schema_version = schema.get("$schema")
        if not isinstance(schema_version, str) or "2020-12" not in schema_version:
            failures.append(f"{rel}: $schema must target draft 2020-12")

        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            failures.append(f"{rel}: schema invalid ({exc.message})")

    for contract, versions in sorted(versions_by_contract.items()):
        unique = sorted(set(versions))
        if len(unique) != len(versions):
            failures.append(f"{contract}: duplicated schema major version found")
            continue
        expected = list(range(unique[0], unique[-1] + 1))
        if unique != expected:
            failures.append(
                f"{contract}: schema major versions must be contiguous, found={unique}"
            )

    if failures:
        print("Schema validation FAILED:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"Schema validation PASSED: {len(files)} schema files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
