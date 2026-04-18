# Contract Changelog Policy

Status: active

This policy defines how contract changes must be recorded in this repository.

## Rules

1. Any change under `jsonschema/**/*.json` must include an update in
   `CONTRACT-CHANGELOG.md` in the same PR/commit.
2. Every changelog entry must include:
   - changed schema path
   - change category (`added`, `changed`, `deprecated`, `removed`, `fixed`)
   - compatibility impact (`backward-compatible` or `breaking`)
   - migration notes if breaking
3. Breaking contract changes require a major schema version bump
   (`*.v1.json` -> `*.v2.json`).
4. Additive, backward-compatible changes should stay in the same major file and
   be documented under `Unreleased`.

## Entry Template

Use this line template in `CONTRACT-CHANGELOG.md`:

`- [<category>] <schema-path> - <compatibility>: <summary> (migration: <notes-or-n/a>)`
