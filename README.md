# platform-contracts
[![CI](https://github.com/waoooolab/platform-contracts/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/waoooolab/platform-contracts/actions/workflows/ci.yml)

Shared contract definitions for runtime services.

Contains:
- jsonschema: request/response/event/tool contracts
- asyncapi: event stream contracts
- protobuf: service contracts (future)

Auth contracts (P0 baseline):
- `jsonschema/auth/token-claims.v1.json`
- `jsonschema/auth/token-exchange.v1.json`
- `jsonschema/auth/device-token.v1.json`
- A7 de-brand retirement schedule:
  - `DEBRAND-COMPATIBILITY-WINDOW.md` (legacy `urn:waoooolab:*` to neutral
    `urn:owa:*` migration timeline)

Runtime contracts (P0 baseline):
- `jsonschema/command-envelope.v1.json` (idempotency + retry semantics)
- `jsonschema/command-envelope.v1.json` and `jsonschema/event-envelope.v1.json`
  include optional split-plane surfaces
  (`communication_memory_trace`, `runtime_state_assembly`) for explicit
  communication-memory vs runtime-state boundary with deterministic recovery
  assembly fields
- `jsonschema/runtime/runtime-state.v1.json` (run/task/device state enums)

Runtime contracts (P6 routing and placement):
- `jsonschema/runtime/execution-profile.v1.json` (control/compute route input)
- `jsonschema/runtime/execution-context.v1.json` (task-plane + executor/runtime context input)
- `jsonschema/runtime/orchestration-hints.v1.json` (run hierarchy + queue priority + scheduling hint input)
- `jsonschema/runtime/context-isolation-contract.v1.json` (canonical context-isolation vocabulary + scenario/orchestration mode mapping acceptance contract)
- `jsonschema/runtime/path-handoff-contract.v1.json` (canonical direct<->orchestrated handoff contract: identity mapping, conflict resolution, and status projection baseline)
- `jsonschema/runtime/scenario-profile-contract.v1.json` (canonical scenario profile contract for `dev_factory`/`visual_factory`/`project_ops` objective, artifact, completion, risk, and orchestration-depth governance)
- `jsonschema/runtime/workflow-template-compile-contract.v1.json` (canonical Product Builder template compile contract for `phase/step` DAG -> workflow task graph with deterministic task-id/dependency policy)
- `jsonschema/runtime/execution-plan-contract.v1.json` (canonical workflow-template -> runtime execution DAG plan output contract with `nodes/edges/entry_point/metadata`)
- `jsonschema/runtime/workflow-template-hitl-profile-policy-contract.v1.json` (canonical Product Builder template-level HITL gate + profile/policy projection contract with deterministic precedence order for submit-envelope projection)
- `jsonschema/runtime/workflow-template-capability-binding-contract.v1.json` (canonical Product Builder template package + capability binding contract with lifecycle metadata and reusable binding resolution policy)
- `jsonschema/runtime/executor-profile-catalog.v1.json` (runtime-supported executor family/engine/adapter catalog output)
- `jsonschema/runtime/tool-catalog.v1.json` (authoritative tool-plane catalog output with `source/provenance/profile/optionality`)
- `jsonschema/runtime/runtime-route-event.v1.json` (`runtime.route.*` events)
- `jsonschema/runtime/runtime-run-event.v1.json` (`runtime.run.requested` + `runtime.run.status` events, including orchestration metadata)
- `jsonschema/runtime/gate-evidence.v1.json` (`runtime.gate.evidence` lifecycle-gate evidence for irreversible transition contracts)
- `jsonschema/runtime/instance-taxonomy.v1.json` (canonical instance/workspace taxonomy contract across deployment/control/runtime planes)
- route/run event payloads may include optional `execution_context` for task-plane and executor/runtime observability
- `jsonschema/runtime/device-route-event.v1.json` (`device.route.*` + `device.lease.*` events)
- canonical executor axis in runtime contracts:
  - `adapter`: `orchestrator|ccb|runtime_api|native`
  - optional `access_mode`: `direct|api`
  - optional `window_mode`: `inline|terminal_mux`

App capability contracts (P6 app-mode baseline):
- `jsonschema/app/app-capability.v1.json` (workflow-to-app publishable capability package, with optional dependency/policy/distribution metadata for capability registry gating)
- `jsonschema/app/app-capability-event.v1.json` (compile/publish/invoke lifecycle events for app capabilities)

AsyncAPI contracts (P6 runtime events baseline):
- `asyncapi/runtime-events.v1.json` (runtime/device event channel catalog with JSON Schema payload refs)

Versioning policy:
- Use SemVer at contract file level (`*.v1.json`, `*.v2.json`).
- Additive fields are backward compatible in the same major version.
- Removing/changing required fields requires a new major version.

Changelog policy:
- Contract changes must update `CONTRACT-CHANGELOG.md` in the same PR.
- See `CONTRACT-CHANGELOG-POLICY.md` for required entry format.

Validation:
- `scripts/validate_schemas.py`: schema syntax + naming + `$id` checks.
- `scripts/validate_asyncapi.py`: asyncapi channel/message and payload-ref checks.
- `scripts/check_changelog_update.py`: changelog policy enforcement.
- `.github/workflows/ci.yml`: cross-platform CI for PR/push
  (Ubuntu/Windows/macOS with Python 3.11 and 3.12).
