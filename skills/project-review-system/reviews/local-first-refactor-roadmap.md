# Local-first Project Review System refactor roadmap

## Review purpose

Review the proposed post-PR6 architecture before implementation. The roadmap is a disposable design artifact: the five-stage review may retain, replace, simplify, split, merge, or remove any proposed element.

## Review mode

Authorized corrective for this review artifact only. No production implementation changes are authorized by this roadmap review.

## Review depth

Full-program five-stage review. One semantic stage per separate execution unit/message.

## Core requirements

1. **Local-first:** every core Project Review System capability must be usable without GitHub Actions or any hosted CI quota.
2. **Deterministic-first:** deterministic local programs own authoritative bookkeeping, hashes, state transitions, coverage accounting, validation, recovery, and completion eligibility wherever those claims are mechanically decidable.
3. **GitHub optional:** GitHub may provide hosting/collaboration; GitHub Actions must be optional and should normally require zero runs. A hosted final verification run may exist only as an optional convenience or assurance layer.
4. **Provider independence:** retrieval, local-model, hosted-model, repository-host, and similar integrations use replaceable capability interfaces. No specific provider is required for core correctness.
5. **Optional local retrieval:** LlamaIndex may be used as a reference retrieval/indexing provider, but semantic retrieval cannot prove exhaustive coverage.
6. **Optional local model:** Phi 14B may assist with bounded semantic preprocessing, classification, extraction, ranking, or candidate generation, but it is not an authority for completion, coverage, hashes, or governance compliance.
7. **Manual fallback:** the core workflow must remain usable when no local model, vector index, hosted model integration, or GitHub service is available, provided a human or other semantic reviewer can supply required judgments.
8. **Semantic/mechanical separation:** the LLM or human reviewer produces semantic judgments; deterministic software owns mechanically enforceable state and validation.
9. **Visible evaluation model:** mapped evaluations must either be explicit in the operating workflow or integrated into stage completion so they do not form a mostly hidden second review layer.
10. **Recoverability:** interrupted work, stale state, reopening, redo, and historical evidence must have deterministic, comprehensible recovery paths.
11. **Low burden:** prefer the smallest architecture that preserves the required guarantees; do not preserve PR6-era complexity merely because it already exists.

## Candidate roadmap to challenge

- deterministic begin/complete/status/resume orchestration;
- simpler active-state versus append-only history representation;
- explicit or stage-integrated mapped evaluations;
- transactional local state transitions;
- removal of redundant prose/manual bookkeeping once mechanically enforced;
- dynamic mid-pass subdivision only after the core state engine is stable;
- optional plug-in providers for retrieval and semantic assistance;
- dogfood and measure the result before claiming the refactor is better.

The review must consider alternatives such as a single append-only event log plus generated views, rather than assuming `active.json`, `occurrences.jsonl`, and `revisions.jsonl` are the correct structure.

## GitHub Actions budget

Normal review operation target: **0 required GitHub Actions runs**.

A design that requires hosted CI to advance, resume, validate, or complete an ordinary review fails this requirement unless the five-stage review explicitly establishes that no local alternative can preserve the required guarantee.

## Reviewer independence

Same-agent self-review. This review may improve the design but is not independent validation.

## Current review state

- Adversarial: In Review
- Interdependency: Pending
- Normalization: Pending
- Structural Optimization: Pending
- End-to-end validation: Pending

No implementation phase or pull-request breakdown is authoritative until the five-stage review completes.
