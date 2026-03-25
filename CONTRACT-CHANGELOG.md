# Contract Changelog

Policy reference:
- `CONTRACT-CHANGELOG-POLICY.md`

## Unreleased

- [changed] jsonschema/command-envelope.v1.json - backward-compatible: add
  optional contract-version fields (`task_contract_version`,
  `agent_contract_version`, `event_schema_version`) so admission/freeze logic
  can bind explicit envelope versions without breaking existing producers
  (migration: fields are optional in v1; producers may roll out gradually)
- [changed] jsonschema/event-envelope.v1.json - backward-compatible: add
  optional contract-version fields (`task_contract_version`,
  `agent_contract_version`, `event_schema_version`) for end-to-end version
  observability on runtime event surfaces (migration: fields are optional in
  v1; event emitters can adopt incrementally)
- [changed] jsonschema/runtime/runtime-run-event.v1.json and
  jsonschema/runtime/runtime-route-event.v1.json - backward-compatible: allow
  optional top-level contract-version fields (`task_contract_version`,
  `agent_contract_version`, `event_schema_version`) so runtime event validators
  remain compatible when envelopes project frozen version bindings (migration:
  fields are optional in v1 and can roll out incrementally)
- [added] jsonschema/runtime/tool-catalog.v1.json - backward-compatible:
  authoritative tool-plane catalog contract (`source`, `provenance`, `profile`,
  `optionality`) for runtime/gateway/control tool catalog parity (migration:
  runtime-execution authoritative catalog endpoint and forwarding surfaces should
  emit `schema_version=tool_catalog.v1`)
- [added] jsonschema/runtime/instance-taxonomy.v1.json - backward-compatible:
  canonical instance/workspace taxonomy contract for deployment/control/runtime
  alignment (`deployment|gateway|runtime_instance|run|session|agent` and
  `mainline_workspace|agent_workspace|lane_workspace|tenant_workspace`) with
  frozen mapping rules (migration: runtime/control responses should expose this
  payload shape when publishing taxonomy metadata)
- [added] jsonschema/runtime/gate-evidence.v1.json - backward-compatible:
  add lifecycle-gate evidence contract (`runtime.gate.evidence`) for
  irreversible transition checks (`lane_cleanup`, branch delete, objective
  archive, policy flip, release finalize) with dual-confirm payload surface and
  control aggregation index hints (`outbox_seq`, `cursor`) (migration: producer
  implementations should emit `task_id`, `gate_status`, `confirmed_at`, and for
  `lane_cleanup` + `passed` provide dual-confirm shas/flags)
- [added] asyncapi/runtime-events.v1.json - backward-compatible: introduce
  machine-readable runtime/device event channel catalog with payload refs to
  existing runtime jsonschema contracts (migration: n/a)
- [changed] jsonschema/runtime/device-route-event.v1.json -
  backward-compatible: add `device.lease.renewed` event type and
  `lease_renewed` decision outcome for explicit lease extension lifecycle
  telemetry (migration: n/a)
- [added] jsonschema/auth/token-claims.v1.json - backward-compatible: baseline
  auth claims contract (migration: n/a)
- [added] jsonschema/auth/token-exchange.v1.json - backward-compatible:
  baseline token exchange request/response contract (migration: n/a)
- [added] jsonschema/auth/device-token.v1.json - backward-compatible: baseline
  device token descriptor contract (migration: n/a)
- [added] jsonschema/command-envelope.v1.json - backward-compatible: baseline
  idempotency + retry command envelope contract (migration: n/a)
- [added] jsonschema/event-envelope.v1.json - backward-compatible: baseline
  runtime event envelope contract (migration: n/a)
- [added] jsonschema/runtime/runtime-state.v1.json - backward-compatible:
  shared run/task/device state enum contract (migration: n/a)
- [added] jsonschema/runtime/execution-profile.v1.json - backward-compatible:
  contract-driven route input for control/compute and placement constraints
  (migration: n/a)
- [added] jsonschema/runtime/execution-context.v1.json - backward-compatible:
  task-plane and executor/runtime context contract for runtime ingress validation
  (migration: n/a)
- [added] jsonschema/runtime/runtime-route-event.v1.json -
  backward-compatible: runtime route decision/failure event contract
  (`runtime.route.decided`, `runtime.route.failed`) (migration: n/a)
- [changed] jsonschema/runtime/runtime-route-event.v1.json -
  backward-compatible: add optional orchestration metadata block
  (`parent_run_id`, `parent_task_id`, `run_depth`, `child_run_ids`,
  cancellation fields) for parent-child telemetry alignment (migration: n/a)
- [added] jsonschema/runtime/runtime-run-event.v1.json -
  backward-compatible: run requested/status event contract
  (`runtime.run.requested`, `runtime.run.status`) with route and
  orchestration payload shape (migration: n/a)
- [changed] jsonschema/runtime/runtime-run-event.v1.json -
  backward-compatible: add optional `payload.execution_context` for task-plane
  and executor/runtime context observability (migration: n/a)
- [changed] jsonschema/runtime/runtime-route-event.v1.json -
  backward-compatible: add optional `payload.execution_context` for route
  decision/failure telemetry alignment (migration: n/a)
- [added] jsonschema/runtime/device-route-event.v1.json -
  backward-compatible: device route and lease lifecycle event contract
  (`device.route.*`, `device.lease.*`) (migration: n/a)
- [added] jsonschema/app/app-capability.v1.json - backward-compatible:
  workflow-to-app publishable capability package contract (migration: n/a)
- [changed] jsonschema/app/app-capability.v1.json - backward-compatible:
  add optional `kind`, `requires_capabilities`, governance policy fields
  (`trust_level`, `policy_profile`), and `distribution` metadata
  (regions/languages/billing profile) for unified registry and scenario gating
  (migration: n/a)
- [added] jsonschema/app/app-capability-event.v1.json - backward-compatible:
  app capability lifecycle event contract for compile/publish/invoke paths
  (migration: n/a)
- [fixed] CONTRACT-CHANGELOG.md - backward-compatible: policy sync checkpoint
  after runtime schema batch push; changelog is now explicitly touched alongside
  schema evolution enforcement workflow (migration: n/a)
- [added] jsonschema/tool-contract.v1.json - backward-compatible: baseline tool
  invocation contract (migration: n/a)
- [changed] jsonschema/runtime/execution-context.v1.json - backward-compatible:
  align executor adapter axis to canonical program values
  (`orchestrator|ccb|runtime_api|native`) and add optional
  `executor.access_mode` (`direct|api`) + `executor.window_mode`
  (`inline|terminal_mux`) for split-axis executor observability
  (migration: n/a)
- [changed] jsonschema/runtime/executor-profile-catalog.v1.json -
  backward-compatible: align `items[].adapters` to canonical execution program
  values and add required `items[].access_modes` + `items[].window_modes`
  arrays (migration: ensure runtime-gateway/runtime-execution profile endpoints
  include the two new fields)
- [changed] jsonschema/runtime/runtime-route-event.v1.json -
  backward-compatible: update nested `payload.execution_context.executor.adapter`
  enum to canonical program values and allow optional nested
  `access_mode/window_mode` (migration: n/a)
- [changed] jsonschema/runtime/runtime-run-event.v1.json -
  backward-compatible: update nested `payload.execution_context.executor.adapter`
  enum to canonical program values and allow optional nested
  `access_mode/window_mode` (migration: n/a)
- [changed] jsonschema/runtime/runtime-run-event.v1.json -
  backward-compatible: add optional route placement trace fields
  (`placement_reason_code`, `placement_reason`, `placement_score`,
  `placement_queue_depth`) for auditable compute routing decisions
  (migration: n/a)
- [added] jsonschema/runtime/runtime-events-page.v1.json - backward-compatible:
  cursor-page response contract for runtime event reads (`items`, `next_cursor`,
  `has_more`, `stats`) to keep gateway/control pagination semantics aligned
  (migration: n/a)
- [added] jsonschema/runtime/runtime-run-lease.v1.json - backward-compatible:
  run lease projection contract (`run_id`, `lease`, `device_hub`) for
  runtime-execution/runtime-gateway/control-gateway lease lookup endpoints
  (migration: n/a)
- [changed] jsonschema/runtime/runtime-events-page.v1.json -
  backward-compatible: add optional `recommended_poll_after_ms` numeric hint
  (100-60000 ms) so event consumers can standardize poll cadence guidance
  directly in page responses (migration: n/a)
- [changed] jsonschema/runtime/runtime-run-lease.v1.json -
  backward-compatible: add optional `recommended_poll_after_ms` numeric hint
  (100-60000 ms) to align lease lookup responses with standardized poll cadence
  guidance across gateway and control forwarding paths (migration: n/a)
- [changed] jsonschema/runtime/runtime-route-event.v1.json -
  backward-compatible: enforce snake_case naming pattern for
  `payload.decision.reason_code`, `payload.failure.code`, and
  `payload.orchestration.failure_reason_code` to reduce cross-service
  diagnostics drift (migration: reason/code fields must match
  `^[a-z0-9_]+$`)
- [changed] jsonschema/runtime/runtime-run-event.v1.json -
  backward-compatible: enforce snake_case naming pattern for
  `payload.route.placement_reason_code` and
  `payload.orchestration.failure_reason_code` (migration: reason/code fields
  must match `^[a-z0-9_]+$`)
- [changed] jsonschema/runtime/device-route-event.v1.json -
  backward-compatible: enforce snake_case naming pattern for
  `payload.decision.reason_code` (migration: reason/code fields must match
  `^[a-z0-9_]+$`)
- [changed] jsonschema/app/app-capability-event.v1.json -
  backward-compatible: enforce snake_case naming pattern for
  `payload.failure.code` (migration: reason/code fields must match
  `^[a-z0-9_]+$`)

## History
