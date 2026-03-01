# Auth Contracts

This directory defines the P0 baseline auth contracts for the waoooolab runtime:

- `token-claims.v1.json`: canonical JWT claim fields
- `token-exchange.v1.json`: request/response contract for delegated tokens
- `device-token.v1.json`: descriptor for node-agent token lifecycle

Implementation notes:
- `runtime-gateway` is the token entry and exchange authority.
- `runtime-execution`, `device-hub`, and `ai-gateway` should validate delegated tokens by `aud` + `scope`.
- Do not distribute provider secrets (`OPENAI_API_KEY`, etc.) through these contracts.
