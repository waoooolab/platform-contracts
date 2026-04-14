# OWA-20260414-610 T3-S2 Stage-A Contract Mapping

## Scope
- Task: `OWA-20260414-610` / Team-3 Stage-C `T3-S2`
- Goal: map Team-2 Stage-A `agent-orchestrator` framework interfaces (LangGraph/LangChain/LangSmith) to existing runtime adapter seams.
- Source inspected (read-only): `/Users/danlio/Repositories/waoooolab/agent-orchestrator` on branch `team2-stage-a`.

## Stage-A Public Contract Surfaces Read
- `src/langgraph_core/service/app.py`
- `src/langgraph_core/service/contracts.py`
- `src/langgraph_core/service/auth.py`
- `src/langgraph_core/engine/base_engine.py`
- `src/langgraph_core/agent/loop.py`
- `src/langgraph_core/kernel/foundation.py`
- `src/langgraph_core/kernel/weighted_scope_scheduler.py`
- `src/langgraph_core/llm/ai_gateway_adapter.py`
- `src/langgraph_core/tracing/langsmith.py`

## Interface-to-Seam Mapping
| Framework runtime path interface (Stage-A) | Existing adapter seam | Status | Mapping rationale |
| --- | --- | --- | --- |
| LangGraph runtime event outputs (`create_runtime_plan`, `create_runtime_decision`) + LangSmith span wrapping | `event_transport` | aligned | Stage-A plan/decision APIs emit canonical runtime event envelopes; runtime event delivery remains governed by runtime-gateway event transport seam. |
| LangGraph service auth boundary (`require_claims`/audience+scope checks) | `runtime_identity` | partial | Stage-A confirms strict bearer claim contract at orchestrator boundary; token issuance/exchange remains implemented through control-gateway runtime identity adapter seam. |
| LangGraph capability registry (`/registry/skills`, `/registry/plugins`) + MCP tool invoke + LangChain runnable tool/model integration | `capability_backend` | aligned | Stage-A capability and tool descriptors map to runtime-execution capability backend operations (`register/list/get/resolve` and tool catalog fetch). |
| LangGraph workflow node dispatch (`dispatch_workflow_node`) + agent loop tool-call decisioning | `workflow_dispatch_backend` | aligned | Stage-A workflow-plane dispatch and tool-call outcomes are the upstream intent/dispatch surface consumed by runtime-governed workflow dispatch backend integration. |
| Weighted scope scheduling + workflow run lifecycle (`start/dispatch/complete`) | `scheduler_backend` | aligned | Stage-A scheduler/workflow kernel defines ordered admission/dispatch semantics that converge with scheduler backend enqueue/tick/registry/cancel seam responsibilities. |

## Evidence Pointers (Representative)
- LangGraph service plan/decision events: `src/langgraph_core/service/app.py:690`, `:709`
- LangGraph workflow lifecycle APIs: `src/langgraph_core/service/app.py:739`, `:794`, `:825`
- Auth contract boundary: `src/langgraph_core/service/auth.py:93`
- Capability registry APIs: `src/langgraph_core/service/app.py:907`, `:941`
- LangGraph workflow dispatch internals: `src/langgraph_core/kernel/foundation.py:600`
- Weighted scheduler interface: `src/langgraph_core/kernel/weighted_scope_scheduler.py:8`
- LangChain runnable adapter: `src/langgraph_core/llm/ai_gateway_adapter.py:22`, `:154`
- LangSmith trace hook: `src/langgraph_core/tracing/langsmith.py:47`, `:63`

## Convergence Summary
- Total mapped seams: 5
- `aligned`: 4 (`event_transport`, `capability_backend`, `workflow_dispatch_backend`, `scheduler_backend`)
- `partial`: 1 (`runtime_identity`)
- Stage-A baseline conclusion: framework/wheel runtime path surfaces are mapped to existing adapter seams, with identity issuance still intentionally anchored in control-gateway runtime identity seam.
