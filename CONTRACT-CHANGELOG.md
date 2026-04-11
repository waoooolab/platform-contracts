# Contract Changelog

Policy reference:
- `CONTRACT-CHANGELOG-POLICY.md`

## Unreleased

- [changed] jsonschema/runtime/runtime-route-event.v1.json and
  jsonschema/runtime/runtime-run-event.v1.json - backward-compatible: debrand
  runtime route target enum values by replacing legacy `langgraph-core` with
  canonical `agent-orchestrator` while preserving existing route semantics and
  adapter compatibility (migration: downstream producers/consumers should emit
  and parse `agent-orchestrator`; legacy aliases remain compatible at control
  ingress during transition)
- [added] jsonschema/runtime/runtime-route-event.v1.json and
  jsonschema/runtime/runtime-run-event.v1.json - backward-compatible: add
  `agent-orchestrator` to `route_target` enum in runtime route/run event
  contracts so agent-orchestrator can be used as a runtime route target
  (migration: n/a)
- [added] catalog/runtime/code-terms.data.v1.json -
  backward-compatible: add canonical code-term normalization policy catalog
  (`snake_case_pattern`, camel-boundary and token cleanup patterns) so
  runtime/control/device services can align reason/failure code normalization
  semantics via shared policy data with local fallback compatibility
  (migration: loaders may adopt incrementally; defaults remain valid)
- [added] catalog/runtime/persistence-paths.data.v1.json -
  backward-compatible: add canonical persistence-path mapping catalog
  (service-level `persist_root_env` + per-path explicit env and relative path)
  so runtime/control/device/ai services can resolve storage paths from one
  shared data source while preserving existing explicit-env precedence
  behavior (migration: loaders may adopt incrementally; hardcoded defaults
  remain fallback)
- [added] catalog/runtime/executor-profile-catalog.data.v1.json -
  backward-compatible: add canonical executor-profile data catalog
  (`family`, `engines`, `adapters`, `access_modes`, `window_modes`) so
  runtime-gateway and runtime-execution can load axis mappings from one
  shared source while keeping existing profile endpoints and validation
  behavior unchanged (migration: consumers may continue using built-in
  defaults and progressively switch to catalog-driven loading)
- [added] jsonschema/runtime/runtime-run-lifecycle-replay.v1.json -
  backward-compatible: add canonical run-scoped lifecycle replay response
  contract (`schema_version`, `run_id`, `items`, `source`,
  `lifecycle_projection`, `dlq_projection`, optional `consumer_cursor`) to
  formalize runtime truth-loop replay reads and prevent generic event-page
  schema drift (migration: additive new schema; runtime-gateway/control
  consumers can adopt incrementally)
- [added] jsonschema/runtime/tenant-config-contract.v1.json -
  backward-compatible: add canonical tenant runtime-config delivery contract
  (`tenant_id`, `chain_policy`, `capability_permissions`,
  `resource_quotas`, `metadata`) for upper-layer product config push into
  control/runtime/ai kernel services (migration: additive new schema;
  producers/consumers can adopt incrementally)
- [added] jsonschema/runtime/execution-plan-contract.v1.json -
  backward-compatible: add canonical workflow-template execution DAG contract
  (`nodes`, `edges`, `entry_point`, `metadata`) for machine-checkable
  template->plan compilation outputs in langgraph-core runtime planning
  (migration: additive new schema; producers/consumers can adopt incrementally)
- [changed] jsonschema/runtime/assistant-decision.v1.json -
  backward-compatible: freeze machine-checkable layered authority and
  deterministic path-promotion contract for assistant orchestration
  (`layered_authority_contract`, `path_promotion_decision_matrix`) with
  neutral upstream plane vocabulary (`agent_orchestrator` /
  `agent_framework` / `external_orchestrator`) and neutral dispatch target
  vocabulary (`agent_orchestrator`/`runtime_execution`/`mixed`), while
  preserving `runtime_execution` as downstream execution-governance truth
  owner (non-peer-parallel); add optional `harness_policy` projection
  (`requirements_requested`, `resolution_status`,
  `required_components`, `resolved_bindings`, optional `resolution_error`)
  so assistant decision payloads can expose harness binding visibility at
  entry boundary (migration: existing payloads remain valid; producers may
  roll out `harness_policy` incrementally)
- [added] jsonschema/runtime/workflow-template-capability-binding-contract.v1.json -
  backward-compatible: add canonical Product Builder template-package and
  capability-binding contract (`template_package`, `capability_bindings`,
  `resolution_policy`) for S6-c/S6-f reusable assembly baseline (migration:
  additive new schema; producers and consumers can adopt incrementally)
- [added] jsonschema/runtime/workflow-template-hitl-profile-policy-contract.v1.json -
  backward-compatible: add canonical Product Builder template-level HITL gate
  and profile/policy projection contract (`template_type`, `hitl`,
  `profile_projection`, deterministic `precedence_order`) for S6-b/S6-d
  submit-envelope projection baseline (migration: additive new schema;
  producers and consumers can adopt incrementally)
- [added] jsonschema/runtime/workflow-template-compile-contract.v1.json -
  backward-compatible: add canonical Product Builder template compile contract
  (`phase/step` DAG -> workflow task graph) with deterministic task-id strategy,
  dependency policy vocabulary, and machine-checkable compile acceptance tokens
  for S6/S6-a kickoff baseline (migration: additive new schema; producers and
  consumers can adopt incrementally)
- [added] jsonschema/runtime/scenario-profile-contract.v1.json -
  backward-compatible: add canonical scenario-profile contract
  (`dev_factory`, `visual_factory`, `project_ops`) with machine-checkable
  objective/artifact mapping, completion-criteria vocabulary, risk-level field,
  orchestration-depth selection, and required policy binding surface (migration:
  additive new schema; producers/consumers can adopt incrementally)
- [added] jsonschema/runtime/path-handoff-contract.v1.json -
  backward-compatible: add canonical dual-path handoff contract for
  `local_direct <-> orchestrated` transition metadata (`handoff_id`,
  source/target identity fields), deterministic identity mapping policy,
  conflict-resolution modes, and status-phase projection baseline
  (migration: additive new schema; producers/consumers can adopt
  incrementally)
- [changed] jsonschema/command-envelope.v1.json and
  jsonschema/event-envelope.v1.json - backward-compatible: add optional
  split-plane contract blocks (`communication_memory_trace`,
  `runtime_state_assembly`) with machine-checkable pairing (`both-or-none`),
  deterministic recovery assembly order, pointer validity, fallback strategy,
  and role/assistant identity fields for S3-b/S3-d baseline closure (migration:
  existing producers remain valid; new split fields are optional and can be
  rolled out incrementally)
- [added] jsonschema/runtime/context-isolation-contract.v1.json -
  backward-compatible: add canonical context-isolation vocabulary contract
  (`scenario_id`, `orchestration_mode`, `context_mode`) with explicit
  communication-memory/runtime-state plane boundaries and acceptance criteria
  for scenario-driven isolation selection (migration: additive new schema;
  consumers can adopt incrementally)
- [changed] jsonschema/runtime/orchestration-hints.v1.json,
  jsonschema/runtime/runtime-run-event.v1.json, and
  jsonschema/runtime/runtime-route-event.v1.json - backward-compatible: add
  optional nested delegation/autonomy governance payloads
  (`nested_leader_contract`, `nested_autonomy_policy`) so outer-leader to
  provider-internal subleader contracts and autonomy handoff policy can be
  validated/projected deterministically without breaking existing producers
  (migration: fields are optional in v1 and can be rolled out incrementally)
- [changed] jsonschema/command-envelope.v1.json and
  jsonschema/event-envelope.v1.json - backward-compatible: add optional
  canonical scope-axis fields (`scope_id`, `scope_type`) while preserving
  legacy tenant/app/session envelope fields for compatibility rollout
  (migration: existing producers remain valid; gateways can start projecting
  scope fields incrementally)
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
- [changed] jsonschema/runtime/runtime-state.v1.json - backward-compatible: add
  `dlq` to `run_status` enum for explicit dead-letter terminal semantics
  (migration: existing statuses unchanged; `dlq` is additive)
- [changed] jsonschema/runtime/runtime-run-event.v1.json and
  jsonschema/runtime/runtime-route-event.v1.json - backward-compatible: add
  optional `payload.compensation_spec` surface and allow `payload.status=dlq`
  for compensation/DLQ contract projections (migration: fields are optional and
  can be emitted incrementally)
- [changed] jsonschema/command-envelope.v1.json - backward-compatible: add
  optional top-level `compensation_spec` contract for submit-time compensation
  plan binding (migration: producers may omit or roll out gradually)
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
- [added] jsonschema/runtime/brownfield-takeover-contract.v1.json -
  backward-compatible: brownfield takeover normalization contract covering
  drift detection (`missing_configs`, `baseline_diff`, `remediation_backlog`),
  workload profile matrix (`dev_profile`, `visual_profile` with checklist and
  acceptance gates), and attach/import lifecycle
  (`source_registration_state`, `identity_mapping`,
  `import_lifecycle_action`) (migration: n/a)
- [added] jsonschema/runtime/observability-early-warning-contract.v1.json -
  backward-compatible: warning-first observability contract for
  chain-specific signals (`queue_depth`, `worker_latency`,
  `resource_utilization`) with threshold/action mapping fields
  (`warn_threshold`, `critical_threshold`, `action_on_warn`,
  `action_on_critical`) (migration: n/a)

## History
