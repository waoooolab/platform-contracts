#!/usr/bin/env python3
"""Validate AsyncAPI runtime events contract and schema references."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "asyncapi" / "runtime-events.v1.json"

EXPECTED_CHANNEL_MESSAGES = {
    "runtime.run": "RuntimeRunEvent",
    "runtime.route": "RuntimeRouteEvent",
    "device.route": "DeviceRouteEvent",
}

EXPECTED_MESSAGE_EVENT_TYPES = {
    "RuntimeRunEvent": {"runtime.run.requested", "runtime.run.status"},
    "RuntimeRouteEvent": {"runtime.route.decided", "runtime.route.failed"},
    "DeviceRouteEvent": {
        "device.route.selected",
        "device.route.rejected",
        "device.lease.acquired",
        "device.lease.released",
        "device.lease.expired",
        "device.lease.renewed",
    },
}


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.as_posix()} must contain a JSON object")
    return payload


def _resolve_internal_ref(spec: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported internal ref: {ref}")
    node: object = spec
    for token in ref[2:].split("/"):
        if not isinstance(node, dict) or token not in node:
            raise ValueError(f"invalid internal ref: {ref}")
        node = node[token]
    if not isinstance(node, dict):
        raise ValueError(f"internal ref target must be object: {ref}")
    return node


def _validate_channels(spec: dict) -> list[str]:
    errors: list[str] = []
    channels = spec.get("channels")
    if not isinstance(channels, dict):
        return ["spec.channels must be object"]

    for channel_name, message_name in EXPECTED_CHANNEL_MESSAGES.items():
        channel = channels.get(channel_name)
        if not isinstance(channel, dict):
            errors.append(f"missing channel: {channel_name}")
            continue
        operation = channel.get("subscribe")
        if not isinstance(operation, dict):
            errors.append(f"channel {channel_name} must define subscribe operation")
            continue
        message = operation.get("message")
        if not isinstance(message, dict):
            errors.append(f"channel {channel_name} subscribe.message must be object")
            continue
        ref = message.get("$ref")
        expected_ref = f"#/components/messages/{message_name}"
        if ref != expected_ref:
            errors.append(
                f"channel {channel_name} message ref mismatch: expected {expected_ref}, got {ref}"
            )
    return errors


def _validate_message_refs(spec: dict) -> list[str]:
    errors: list[str] = []
    components = spec.get("components")
    if not isinstance(components, dict):
        return ["spec.components must be object"]
    messages = components.get("messages")
    if not isinstance(messages, dict):
        return ["spec.components.messages must be object"]

    for message_name, expected_event_types in EXPECTED_MESSAGE_EVENT_TYPES.items():
        message = messages.get(message_name)
        if not isinstance(message, dict):
            errors.append(f"missing message component: {message_name}")
            continue

        payload = message.get("payload")
        if not isinstance(payload, dict):
            errors.append(f"message {message_name} payload must be object")
            continue
        ref = payload.get("$ref")
        if not isinstance(ref, str) or not ref:
            errors.append(f"message {message_name} payload.$ref must be non-empty string")
            continue

        schema_path = (SPEC_PATH.parent / ref).resolve()
        if not schema_path.is_file():
            errors.append(f"message {message_name} schema ref not found: {ref}")
            continue

        schema = _load_json(schema_path)
        event_type = schema.get("properties", {}).get("event_type", {})
        enum_values = event_type.get("enum")
        if not isinstance(enum_values, list) or not enum_values:
            errors.append(f"message {message_name} schema missing event_type enum: {schema_path.as_posix()}")
            continue
        actual = {str(value) for value in enum_values}
        if actual != expected_event_types:
            errors.append(
                f"message {message_name} event_type enum mismatch: "
                f"expected={sorted(expected_event_types)} actual={sorted(actual)}"
            )
    return errors


def main() -> int:
    if not SPEC_PATH.is_file():
        print(f"FAIL asyncapi-validate: missing spec file {SPEC_PATH.as_posix()}")
        return 1

    try:
        spec = _load_json(SPEC_PATH)
    except Exception as exc:  # pragma: no cover - defensive parse failure path
        print(f"FAIL asyncapi-validate: failed to parse spec: {exc}")
        return 1

    errors: list[str] = []
    if str(spec.get("asyncapi", "")).strip() != "2.6.0":
        errors.append("spec.asyncapi must equal 2.6.0")
    if str(spec.get("defaultContentType", "")).strip() != "application/json":
        errors.append("spec.defaultContentType must equal application/json")
    errors.extend(_validate_channels(spec))
    errors.extend(_validate_message_refs(spec))

    if errors:
        for error in errors:
            print(f"FAIL asyncapi-validate: {error}")
        print(f"asyncapi-validate summary: errors={len(errors)}")
        return 1

    print(
        "asyncapi-validate summary: "
        f"channels={len(EXPECTED_CHANNEL_MESSAGES)} messages={len(EXPECTED_MESSAGE_EVENT_TYPES)} errors=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
