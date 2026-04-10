# platform-contracts AGENTS.md

## Service Description
Shared contract authority repository for schema/event/catalog artifacts used by runtime and control-plane services.

## Entrypoints
- `README.md` - contract lifecycle overview and repository usage.
- `scripts/validate_schemas.py` - JSON schema validation entry.
- `scripts/validate_asyncapi.py` - AsyncAPI contract validation entry.
- `scripts/check_changelog_update.py` - changelog policy enforcement entry.

## Key Modules
- `jsonschema/runtime/` - runtime data contracts and guard-facing schemas.
- `jsonschema/auth/` - token, claim, and exchange contract schemas.
- `asyncapi/runtime-events.v1.json` - runtime event channel contract.
- `catalog/runtime/` - runtime catalog data contracts and governed dictionaries.

## Common Commands
- `python3 scripts/validate_schemas.py`
- `python3 scripts/validate_asyncapi.py`
- `python3 scripts/check_changelog_update.py`
- `python3 scripts/governance/guards/check_governance_guard.py`

## ACP Provider Playbook

### Claude Code (claude)
- Start/Connection: Register provider id `claude` in consuming services and load Anthropic credentials from managed secrets.
- Best Practices: Use contract-first prompts, strict schema citations, and deterministic response requirements.
- Known Limitations/Notes: Large schema context can increase latency and token usage; keep prompt scope bounded.
- Suitable Scenarios: Deep contract reasoning, migration impact analysis, and policy-sensitive design reviews.

### Codex
- Start/Connection: Register provider id `codex` via OpenAI-compatible adapter in consuming services.
- Best Practices: Request structured JSON outputs tied to explicit contract ids and versions.
- Known Limitations/Notes: Broad prompts can produce non-canonical field naming; always validate against schema.
- Suitable Scenarios: Contract authoring assistance, migration patch generation, and validation script prototyping.

### Gemini
- Start/Connection: Register provider id `gemini` with Google AI credential routing in provider config.
- Best Practices: Split prompts by contract family and include expected version/source anchors.
- Known Limitations/Notes: Output structure rigor may vary by model variant; run schema validation on every result.
- Suitable Scenarios: Long-context contract diffing, semantic clustering, and cross-document synthesis.

### OpenCode (droid)
- Start/Connection: Register provider id `droid` and connect through ACP transport with repository/workspace context.
- Best Practices: Keep tooling allowlists minimal and run all generated artifacts through validation scripts.
- Known Limitations/Notes: Interactive session state may reset on reconnect; persist intermediate artifacts explicitly.
- Suitable Scenarios: Tool-assisted repository surgery, scripted validation loops, and operator-guided contract updates.

### Other Mainstream ACP Providers
- Start/Connection: Integrate additional providers via OpenAI-compatible adapters (Azure OpenAI, enterprise proxy gateways, local inference backends).
- Best Practices: Normalize provider outputs to one contract format and gate merges with validation scripts.
- Known Limitations/Notes: Tokenization/context-window differences can alter output shape; do not skip schema checks.
- Suitable Scenarios: Private-network operation, compliance-constrained environments, and cost-tiered provider routing.
