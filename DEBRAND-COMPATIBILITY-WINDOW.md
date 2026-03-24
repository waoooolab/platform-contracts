# A7 De-Brand Compatibility Window

Date: 2026-03-24
Scope: `platform-contracts` token-exchange contract family (`S16-i`)

## Current Baseline (`token-exchange.v1`)

The v1 auth contract keeps legacy URN tokens as frozen values:

- `urn:waoooolab:params:oauth:grant-type:token-exchange`
- `urn:waoooolab:token-type:service_token`
- `urn:waoooolab:token-type:device_token`

This freeze avoids breaking existing runtime-gateway/control integrations that
already emit and validate those values.

## Neutral Target

Target neutral URNs for de-brand migration:

- `urn:owa:params:oauth:grant-type:token-exchange`
- `urn:owa:token-type:service_token`
- `urn:owa:token-type:device_token`

These neutral values are planned for a new contract revision, not an in-place
`v1` mutation.

## Retirement Window

1. Through 2026-06-30:
   - Keep `token-exchange.v1` legacy URNs as the compatibility baseline.
2. Starting 2026-07-01:
   - Introduce neutral URNs in a new token-exchange contract version with
     explicit compatibility acceptance for legacy values.
3. Not earlier than 2026-10-01:
   - Remove legacy URNs from defaults after one release window of
     dual-acceptance and guard verification.

## Guard Tie-In

`openwaoooo/scripts/guards/orchestrator/check_a7_debrand_guard.py` enforces
that this window document remains present and date-pinned.
