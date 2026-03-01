# platform-contracts

Shared contract definitions for runtime services.

Contains:
- jsonschema: request/response/event/tool contracts
- asyncapi: event stream contracts (future)
- protobuf: service contracts (future)

Auth contracts (P0 baseline):
- `jsonschema/auth/token-claims.v1.json`
- `jsonschema/auth/token-exchange.v1.json`
- `jsonschema/auth/device-token.v1.json`

Runtime contracts (P0 baseline):
- `jsonschema/command-envelope.v1.json` (idempotency + retry semantics)
- `jsonschema/runtime/runtime-state.v1.json` (run/task/device state enums)

Versioning policy:
- Use SemVer at contract file level (`*.v1.json`, `*.v2.json`).
- Additive fields are backward compatible in the same major version.
- Removing/changing required fields requires a new major version.
