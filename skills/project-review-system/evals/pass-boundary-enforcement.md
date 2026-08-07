# Evaluation: Pass-Boundary Enforcement

## Purpose

Verify that a credited Adaptive Execution pass cannot be represented as merely another checklist item inside one undifferentiated semantic execution. Each credited pass must have a distinct declared execution unit, must externalize a bounded handoff that the next pass explicitly consumes, and in repository execution must leave ordered durable evidence rather than being backfilled together after the fact.

## Required behavior

1. Every credited execution-plan pass has a nonempty `execution_unit_id`.
2. Execution-unit identifiers are unique within the revalidation record.
3. Every credited pass records a boundary kind and boundary ID; boundary identities are unique within the record.
4. A pass produces a bounded handoff containing findings, evidence references when applicable, unresolved conditions when applicable, and its exact downstream consumer.
5. The handoff is hashed canonically and the recorded hash must match its contents.
6. Except for the first credited pass, each pass records the exact previous handoff hash as `inbound_handoff_sha256`.
7. A later required stage cannot receive passing credit while an earlier required stage remains unpassed.
8. An `ISOLATED` pass requires an `isolated-context` boundary declaration; a non-isolated pass may not claim that boundary kind.
9. The final credited pass hands off to `review-completion`.
10. In repository execution, the current gate must already exist in a prior durable change-record state before the pass first receives credit.
11. Two distinct passes may not first receive credit in the same change-record commit.
12. Before a later pass first receives credit, the exact previous pass handoff must already exist in the prior durable change-record state.
13. In a chat host where one assistant message is the selected SEPARATED execution unit, perform only one semantic pass per assistant message and put its bounded findings/handoff in that message or a durable artifact read by the next pass before it begins.

## Failure conditions

Fail if:

- two credited passes reuse the same execution-unit or boundary identity;
- a later pass does not consume the previous pass handoff;
- handoff contents can change without invalidating their hash;
- stage credit skips an earlier required stage;
- an ISOLATED pass is recorded without an isolation boundary;
- a pass receives durable credit before its current gate existed in a prior change-record state;
- two passes are first credited together in one change-record commit;
- the exact prior handoff was not durably present before the next pass received credit;
- multiple semantic stages are executed in one undifferentiated assistant message while being recorded as separate passes; or
- the repository claims that its deterministic checker proves a host message/context boundary when the host supplied no independently meaningful boundary ID.

## Assurance boundary

The deterministic checker can prove consistency of the recorded execution-unit identities, handoff chain, order, hashes, and—inside Git repository execution—the durable chronology of gate-before-credit and one-credit-commit-per-pass. It cannot independently prove that a ChatGPT message boundary or fresh context actually occurred unless the execution host exposes a trustworthy boundary identifier. Where no such identifier exists, the boundary identity remains an attestation, but Git chronology prevents several passes from being backfilled as separately completed in one final record state.
