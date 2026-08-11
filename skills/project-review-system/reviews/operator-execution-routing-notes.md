# Operator Execution Routing Notes

> Non-authoritative living note for Project Review System dogfooding and local-first redesign. Current validated PRS behavior remains authoritative until formally reviewed and adopted.

## Connector-first execution rule

Observed dogfooding failure: work was unnecessarily bounced to Codex for a bookkeeping/gate step even though the active ChatGPT session already had sufficient GitHub connector capability to perform the operation and continue the governed semantic stage after the gate became durable.

Operational rule for future PRS work:

1. Before delegating a step to Codex or another external execution environment, first determine whether the current ChatGPT session can complete it safely with the available connector/tools.
2. Keep work in the current session when the connector can reliably perform the required repository reads/writes and the task does not require a local checkout, local process execution, CI log inspection, or another unavailable capability.
3. Use Codex/local execution only for work that genuinely requires capabilities unavailable in the current session, especially deterministic repository commands, local tests, queue generation, Git worktree/index inspection, or other checkout-dependent operations.
4. A durable semantic-stage gate must exist before the semantic pass begins, but gate creation and semantic review do not need different agents. Once a gate is durably committed and verified, the current reviewer should continue directly into the authorized semantic pass when capable.
5. Preserve semantic-pass separation: one governed semantic stage per assistant message/execution boundary when the current PRS requires separated execution. Connector-first routing must not collapse required semantic boundaries.
6. Do not make the user act as a manual transport layer between ChatGPT and Codex when one of the agents can safely perform the synchronization itself.
7. When a delegated Codex/local task is used, include explicit recovery behavior for predictable environment limits (for example, retrying a permitted Git fetch outside the sandbox when sandbox networking is unavailable) rather than stopping prematurely.

Preferred decision order:

```text
required PRS action
      ↓
Can current ChatGPT tools safely do it?
      ├─ yes → do it here
      └─ no  → delegate the smallest checkout/local-only step
                    ↓
             return durable result
                    ↓
             continue here if capable
```

This rule is intended to reduce unnecessary model/context switching, user handoffs, latency, and usage while preserving PRS gates, chronology, deterministic validation, and semantic separation.
