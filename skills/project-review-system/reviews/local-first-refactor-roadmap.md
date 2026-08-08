# Local-first Project Review System refactor roadmap

## Review purpose

Review the proposed post-PR6 architecture before implementation. The roadmap is a disposable design artifact: the five-stage review may retain, replace, simplify, split, merge, or remove any proposed element.

## Review mode

Authorized corrective for this review artifact only. No production implementation changes are authorized by this roadmap review.

## Review depth

Full-program five-stage review. One semantic stage per separate execution unit/message.

## Core requirements

1. **Local-first:** every core Project Review System review capability must be usable without GitHub Actions or any hosted CI quota.
2. **Deterministic-first:** deterministic local programs own authoritative bookkeeping, hashes, state transitions, coverage accounting, validation, recovery, and completion eligibility wherever those claims are mechanically decidable.
3. **GitHub optional:** GitHub may provide hosting/collaboration; GitHub Actions must be optional and should normally require zero runs. A hosted final verification run may exist only as an optional convenience or additional assurance layer.
4. **Provider independence:** retrieval, local-model, hosted-model, repository-host, and similar integrations use replaceable capability interfaces. No specific provider is required for core correctness.
5. **Provider trust boundary:** plug-in providers receive only the minimum capabilities and scoped inputs needed for their declared role. Retrieval/model/provider output is untrusted evidence or proposal unless an explicitly defined authority says otherwise; a provider cannot grant itself workflow authority, completion credit, repository permissions, or coverage claims.
6. **Optional local retrieval:** LlamaIndex may be used as a reference retrieval/indexing provider, but semantic retrieval cannot prove exhaustive coverage and cannot silently define the complete review scope.
7. **Optional local model:** Phi 14B may assist with bounded semantic preprocessing, classification, extraction, ranking, or candidate generation, but it is not an authority for completion, coverage, hashes, governance compliance, or permissions.
8. **Manual fallback:** the core workflow must remain usable when no local model, vector index, hosted model integration, or GitHub service is available, provided a human or other semantic reviewer can supply required judgments.
9. **Semantic/mechanical separation:** the LLM or human reviewer produces semantic judgments; deterministic software owns mechanically enforceable state and validation.
10. **Visible evaluation model:** mapped evaluations must either be explicit in the operating workflow or integrated into stage completion so they do not form a mostly hidden second review layer.
11. **Recoverability:** interrupted work, stale state, reopening, redo, and historical evidence must have deterministic, comprehensible recovery paths.
12. **Low burden:** prefer the smallest architecture that preserves the required guarantees; do not preserve PR6-era complexity merely because it already exists.
13. **Assurance separation:** local validation may establish that the Project Review System's own review state and evidence satisfy its rules, but it must not claim to enforce a remote host's merge/branch policy. Preventing a privileged user from bypassing local checks is a repository-host control and may require optional host-side branch protection or CI. Core review correctness must not depend on that host enforcement.

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

A design that requires hosted CI to advance, resume, validate, or complete an ordinary review fails this requirement unless the five-stage review explicitly establishes that no local alternative can preserve the required review guarantee.

Optional host-side enforcement may be used to prevent remote merge-policy bypass, but that is a separate assurance layer from local review correctness and must not be required to use the Project Review System itself.

## Adversarial findings

**Verdict: Complete.** Same-agent self-review; no independent-validation claim.

Material attacks covered:

- **Hosted-CI dependency / quota denial:** a required GitHub Actions path could make the system unusable after quota exhaustion. Corrected requirement: normal review operation must require zero hosted runs.
- **Remote-enforcement overclaim:** local checks cannot prevent a privileged remote-repository user from bypassing local policy. Corrected requirement: distinguish local review validity from optional host-enforced merge protection.
- **Provider authority injection:** a retrieval/model plug-in could otherwise become an accidental authority or permission-expansion path. Corrected requirement: least-privilege provider interfaces and untrusted outputs by default.
- **Retrieval omission:** LlamaIndex or another semantic index can miss material files or relationships. Retained rule: retrieval assists navigation but cannot prove exhaustive coverage or silently define complete scope.
- **Local-model overclaim:** Phi 14B or another helper could produce plausible but unsupported classifications. Retained rule: local-model output is candidate semantic assistance, never mechanical completion/coverage/governance authority.
- **Provider lock-in:** hard-coding LlamaIndex, Phi, ChatGPT, GitHub, Ollama, LM Studio, or another implementation would violate portability. Retained provider-capability interface requirement plus manual fallback.
- **Opaque automation:** moving bookkeeping into software could hide invalid semantic judgments. Retained semantic/mechanical separation: automation can enforce recorded consequences, not prove semantic correctness.
- **Interrupted/stale workflow:** automation that cannot deterministically resume/reopen would recreate PR6-era state hazards. Retained recoverability as a core invariant.
- **Architecture anchoring:** the candidate file split or command list might be preserved merely because it was proposed first. The roadmap remains explicitly disposable; Structural Optimization must compare alternative state models.

No additional blocking Adversarial defect remains in the corrected roadmap's accessible bounded scope. Non-blocking implementation details are deferred to later stages rather than being prematurely designed here.

## Reviewer independence

Same-agent self-review. This review may improve the design but is not independent validation.

## Current review state

- Adversarial: Complete
- Interdependency: Ready
- Normalization: Pending
- Structural Optimization: Pending
- End-to-end validation: Pending

## Next bounded handoff

Interdependency must map the proposed local state engine, semantic reviewer, retrieval provider, model provider, Git/GitHub layers, evaluations, history, recovery, and optional host enforcement as producers/consumers/authorities. It must determine which current PR6 controls are replaced, retained, generated, or made optional before any implementation architecture is selected.

No implementation phase or pull-request breakdown is authoritative until the five-stage review completes.
