#!/usr/bin/env python3
"""Validate mem0 seam schemas and adapter catalog entry."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "jsonschema" / "runtime"
CATALOG_PATH = ROOT / "catalog" / "runtime" / "adapter-seams.data.v1.json"

STORE_SCHEMA_PATH = RUNTIME_DIR / "memory-store-request.v1.json"
EVENT_SCHEMA_PATH = RUNTIME_DIR / "memory-memory-event.v1.json"

STORE_FIELDS = {
    "tenant_id",
    "user_id",
    "session_id",
    "memory_key",
    "content",
    "metadata",
    "created_at",
    "updated_at",
}
STORE_REQUIRED = {
    "tenant_id",
    "user_id",
    "session_id",
    "memory_key",
    "content",
    "created_at",
}

EVENT_FIELDS = {
    "event_type",
    "tenant_id",
    "user_id",
    "session_id",
    "memory_key",
    "content",
    "metadata",
    "timestamp",
    "request_id",
    "service",
    "env",
}
EVENT_REQUIRED = {
    "event_type",
    "tenant_id",
    "user_id",
    "session_id",
    "memory_key",
    "timestamp",
    "service",
    "env",
}


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.as_posix()}: root must be a JSON object")
    return payload


def _expect(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _validate_schema(
    *,
    path: Path,
    expected_id_suffix: str,
    expected_fields: set[str],
    expected_required: set[str],
    failures: list[str],
) -> None:
    if not path.is_file():
        failures.append(f"missing schema file: {path.as_posix()}")
        return

    schema = _load_json(path)
    rel = path.relative_to(ROOT).as_posix()

    _expect(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{rel}: $schema mismatch", failures)
    schema_id = schema.get("$id")
    _expect(isinstance(schema_id, str) and schema_id.endswith(expected_id_suffix), f"{rel}: $id must end with {expected_id_suffix}", failures)
    _expect(schema.get("type") == "object", f"{rel}: type must be object", failures)

    properties = schema.get("properties")
    _expect(isinstance(properties, dict), f"{rel}: properties must be an object", failures)
    if isinstance(properties, dict):
        property_names = set(properties.keys())
        _expect(expected_fields.issubset(property_names), f"{rel}: missing properties {sorted(expected_fields - property_names)}", failures)

    required = schema.get("required")
    _expect(isinstance(required, list), f"{rel}: required must be an array", failures)
    if isinstance(required, list):
        required_names = {str(item) for item in required}
        _expect(expected_required.issubset(required_names), f"{rel}: missing required fields {sorted(expected_required - required_names)}", failures)



def _validate_catalog(failures: list[str]) -> None:
    if not CATALOG_PATH.is_file():
        failures.append(f"missing catalog file: {CATALOG_PATH.as_posix()}")
        return

    catalog = _load_json(CATALOG_PATH)
    seams = catalog.get("seams")
    if not isinstance(seams, list):
        failures.append("catalog/runtime/adapter-seams.data.v1.json: seams must be an array")
        return

    matches = [item for item in seams if isinstance(item, dict) and item.get("id") == "memory_backend"]
    _expect(len(matches) == 1, "catalog/runtime/adapter-seams.data.v1.json: exactly one seam with id=memory_backend is required", failures)
    if len(matches) != 1:
        return

    seam = matches[0]
    _expect(seam.get("protocol") == "MemoryBackendAdapter", "memory_backend: protocol must be MemoryBackendAdapter", failures)

    convergence_status = seam.get("convergence_status")
    _expect(isinstance(convergence_status, dict), "memory_backend: convergence_status must be an object", failures)
    if isinstance(convergence_status, dict):
        stage_a = convergence_status.get("stage_a")
        _expect(isinstance(stage_a, dict), "memory_backend: convergence_status.stage_a must be an object", failures)
        if isinstance(stage_a, dict):
            _expect(stage_a.get("status") == "defined", "memory_backend: convergence_status.stage_a.status must be defined", failures)


def validate() -> int:
    failures: list[str] = []

    _validate_schema(
        path=STORE_SCHEMA_PATH,
        expected_id_suffix="/runtime/memory-store-request.v1.json",
        expected_fields=STORE_FIELDS,
        expected_required=STORE_REQUIRED,
        failures=failures,
    )
    _validate_schema(
        path=EVENT_SCHEMA_PATH,
        expected_id_suffix="/runtime/memory-memory-event.v1.json",
        expected_fields=EVENT_FIELDS,
        expected_required=EVENT_REQUIRED,
        failures=failures,
    )
    _validate_catalog(failures)

    if failures:
        print("validate_seam_schemas: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("validate_seam_schemas: OK")
    print(f"- schema: {STORE_SCHEMA_PATH.relative_to(ROOT).as_posix()}")
    print(f"- schema: {EVENT_SCHEMA_PATH.relative_to(ROOT).as_posix()}")
    print(f"- catalog seam: memory_backend")
    print("- stage_a.status: defined")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
