# Contract Changelog

Policy reference:
- `CONTRACT-CHANGELOG-POLICY.md`

## Unreleased

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

## History
