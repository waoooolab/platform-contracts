# OWA-20260414-610 T3-S3 Stage-B Contract Mapping

## Scope
- Task: `OWA-20260414-610` / Team-3 Stage-C `T3-S3`
- Goal: validate Team-1 Stage-B AI-Gateway control-plane integration against existing runtime adapter seams and confirm six-field metadata passthrough chain closure.
- Source inspected (read-only): `/Users/danlio/Repositories/waoooolab/ai-gateway` on branch `team1-stage-b`.

## Stage-B Public Contract Surfaces Read
- `ai-gateway/src/ai_gateway/service/app.py`
- `ai-gateway/src/ai_gateway/service/gateway_payload_utils.py`
- `control-gateway/src/control_gateway/consumer_entry_forwarding.py`
- `control-gateway/src/control_gateway/runtime_forwarding.py`
- `runtime-execution/src/runtime_execution/service_api/control_ingress.py`
- `runtime-execution/src/runtime_execution/service_api/route_events.py`
- `runtime-execution/src/runtime_execution/service_api/run_status.py`
- `control-gateway/tests/test_consumer_entry_forwarding.py`
- `runtime-execution/tests/test_service_api_execution_context.py`

## Six-Field Passthrough Verification
Metadata chain under verification:
- `tenant_id`
- `team_id`
- `service`
- `env`
- `request_id`
- `cost_center`

Evidence summary:
- AI-Gateway declares and filters exactly these six metadata keys in `_LITELLM_METADATA_KEYS` and `_build_litellm_metadata` (`ai_gateway/service/app.py:54-61`, `:147-181`).
- AI-Gateway only injects metadata when gateway methods support it (`ai_gateway/service/gateway_payload_utils.py:24-29`, `ai_gateway/service/app.py:239-246`).
- Control-gateway consumer-entry forwarding builds and merges the same six fields for AI completion forwarding (`control_gateway/consumer_entry_forwarding.py:45-89`) and tests assert all six (`tests/test_consumer_entry_forwarding.py:96-102`).
- Runtime forwarding preserves caller-provided ingress payload fields by starting from existing `control_ingress` and overlaying required core ingress contract fields (`control_gateway/runtime_forwarding.py:633-661`, `:2021-2037`, `:2118-2134`).
- Runtime-execution projects optional metadata fields from `control_ingress`/payload/metadata into canonical event payloads (`runtime_execution/service_api/control_ingress.py:22-28`, `:66-132`) and emits them in both route and run-status events (`route_events.py:225-239`, `run_status.py:137-145`).
- Runtime-execution tests assert all six fields in submit and status event payloads (`tests/test_service_api_execution_context.py:154-158`, `:174-178`, `:225-229`).

Conclusion: Stage-B six-field passthrough chain is complete across AI-Gateway -> control-gateway -> runtime-execution runtime event projection path.

## Adapter-Seam Mapping
| Stage-B runtime path interface | Existing adapter seam | Status | Mapping rationale |
| --- | --- | --- | --- |
| AI-Gateway metadata normalization and optional passthrough (`_build_litellm_metadata`, completion/embedding metadata support) | `event_transport` | aligned | Runtime event payloads carry canonical `control_ingress` metadata that the runtime event transport seam delivers unchanged. |
| Delegated control-plane claims + metadata assembly (`_build_ai_completion_metadata`, `_metadata_field`) | `runtime_identity` | partial | Stage-B confirms identity claims are consumed for metadata propagation; token issuance/exchange backend remains governed by runtime_identity adapter seam. |
| Runtime forwarding `control_ingress` injection and runtime projection (`_build_control_ingress_contract`, `project_control_ingress`) | `capability_backend` | aligned | Capability-plane runtime events now consistently include six-field metadata in canonical `control_ingress` payload. |
| Run/objective forwarding path (`forward_runtime_run_create`, `forward_control_objective_start`) | `workflow_dispatch_backend` | aligned | Workflow dispatch ingress preserves and projects six-field metadata across control-plane to runtime event boundaries. |
| Run status emission + ingress metadata extraction (`build_run_status_event`, `_extract_request_control_ingress_metadata`) | `scheduler_backend` | aligned | Scheduler/status lifecycle telemetry keeps six-field attribution available for downstream audit and observability. |

## Fixture Drift Resolution
Observed drift before fix:
- `runtime-execution` fixture files already contained optional `control_ingress` metadata fields.
- `platform-contracts/jsonschema/runtime/runtime-route-event.v1.json` and `runtime-run-event.v1.json` were behind (missing these optional metadata properties), causing `runtime-execution/tests/test_contract_fixture_sync.py` failures.

Resolution applied:
- Aligned platform canonical runtime schemas with fixture shape by adding optional `control_ingress` properties:
  - `team_id`
  - `service`
  - `env`
  - `request_id`
  - `cost_center`
- Re-ran fixture sync validation to confirm no drift remains.

## Stage-B Convergence Summary
- Total seams evaluated: 5
- `aligned`: 4 (`event_transport`, `capability_backend`, `workflow_dispatch_backend`, `scheduler_backend`)
- `partial`: 1 (`runtime_identity`)
- Baseline: Stage-B control-plane integration is converged for six-field metadata passthrough and reflected in adapter seam catalog `convergence_status.stage_b`.
