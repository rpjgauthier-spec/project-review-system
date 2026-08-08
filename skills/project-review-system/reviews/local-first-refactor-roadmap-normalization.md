# Local-first refactor roadmap — Normalization review

## Scope

Normalization of the post-PR6 refactor roadmap after Adversarial and Interdependency. This stage aligns concepts and terminology without selecting the final persistence model, plug-in framework, command layout, or implementation decomposition.

## Verdict

**Complete.** Same-agent self-review; no independent-validation claim.

## Canonical vocabulary for the roadmap

### Review target and state

- **Reviewed snapshot** — the exact source state being reviewed. This is the semantic concept consumed by inventory, retrieval, semantic work, and evidence.
- **Snapshot ID** — the canonical machine identity assigned to a reviewed snapshot by the snapshot authority. Do not alternate among `target state`, `artifact state`, `source snapshot`, `repository state`, and `current target` when the same concept is meant.
- **Workflow state** — the authoritative current state of the review process: revision, stage/pass position, required work, completion eligibility, conflicts, and reopening state.
- **Current projection** — a human- or machine-readable view derived from authoritative workflow state/history. Status screens and generated queues are projections unless explicitly made authoritative by the final architecture.
- **Historical evidence** — durable evidence of prior semantic and mechanical occurrences. It is not current workflow state and cannot advance the workflow by itself.
- **Occurrence** — one logically distinct credited execution/event whose identity must not be replaced or replayed without the defined revision/reopening rules.

### Semantic versus mechanical concepts

- **Semantic reviewer** — a human or model that makes bounded semantic judgments. A model is not automatically a separate authority merely because it is a different implementation.
- **Semantic result** — a bounded judgment/finding/verdict supplied through the reviewer contract.
- **Mechanical evidence** — deterministically checkable facts such as snapshot identity, schema validity, inventory/range coverage records, transition preconditions, hashes, ordering, and conflict state.
- **Completion eligibility** — the deterministic conclusion that all mechanically required prerequisites for a transition are satisfied. This is not proof that the semantic result is correct.
- **Review completion** — the workflow-level terminal state after all required semantic results, evaluations/acceptance criteria, and mechanical prerequisites are satisfied. Do not use `validated`, `passed`, `clear`, or `complete` interchangeably across these layers.

### Providers and adapters

- **Provider** — a replaceable implementation that supplies a declared capability, such as retrieval or semantic review. Examples may include LlamaIndex, Phi, ChatGPT, Claude, a human reviewer, or a future implementation.
- **Provider adapter** — the code that translates a provider-specific API/format into the Project Review System's provider-neutral contract. The provider and adapter are distinct: an adapter may be trusted code while provider output remains untrusted semantic evidence/proposal.
- **Provider capability** — one narrowly declared function exposed through the neutral contract, such as retrieval or semantic review. Capability advertisement does not grant permission.
- **Provider configuration** — user-controlled configuration that selects/enables providers, grants allowed capabilities, and governs data egress. Repository content cannot own or silently mutate it.
- **Plug-in** — reserve this term for executable extension code that is installed/enabled into the local system. Do not use `plug-in` as a synonym for every provider or remote service; doing so confuses code-execution risk with ordinary provider substitution.
- **Repository host** — GitHub, GitLab, a local forge, or another collaboration/hosting system. It is not a semantic reviewer, state backend, or workflow authority merely because it stores the repository.
- **Persistence backend** — the implementation that stores workflow state/history. SQLite, files, Git-backed storage, or another mechanism are candidate backends, not competing workflow authorities.

### Retrieval and coverage

- **Retrieval** — selection of potentially relevant content for navigation/context. Semantic search, LlamaIndex, grep-like search, or another provider may implement it.
- **Inventory** — deterministic accounting of objects/items that exist within the declared scope when such accounting is required.
- **Coverage** — evidence that required scoped items/ranges received the declared processing. Retrieval is not coverage and a retrieval provider cannot establish exhaustive coverage merely by returning results.
- **Index snapshot** — the reviewed snapshot ID to which a retrieval index/cache is bound. A stale index is not a current retrieval result even if its internal database is consistent.

### Review structure

- **Stage** — one of the five canonical semantic review lenses: Adversarial, Interdependency, Normalization, Structural Optimization, End-to-end validation.
- **Pass** — one bounded execution unit within a stage.
- **Subpass** — a pass created by subdividing stage work while preserving stage identity, prior state, ordering, and handoff requirements.
- **Evaluation / acceptance criterion** — the roadmap does not yet choose whether the existing mapped evaluations remain independent workflow items or become explicit stage acceptance criteria. Until Structural Optimization decides this, use `evaluation` when referring to the current system and `acceptance criterion` only for the possible integrated future representation. Do not treat them as two simultaneous required layers unless deliberately designed that way.
- **Breadth evidence** — structured evidence that a full-program stage covered the applicable canonical analysis surface, including explicit N/A dispositions and the scope-inversion/breadth check. It demonstrates required coverage accounting, not semantic quality.

### Local and hosted assurance

- **Local review correctness** — satisfaction of Project Review System workflow rules using local mechanisms, with no required hosted CI quota.
- **Host enforcement** — optional repository-host controls that prevent or detect bypass of merge/branch policy. This is a separate assurance layer.
- **Hosted verification** — optional remote execution that independently repeats selected checks. It must not be required for ordinary review completion.
- **Tamper evidence** — evidence useful for detecting accidental or unauthorized alteration under stated assumptions. Do not use `tamper-proof` or `non-repudiation` for a fully user-controlled local environment unless an external trust mechanism actually supplies that property.

## Normalization findings and dispositions

1. **`target state` / `artifact state` / `source snapshot` / `repository state` drift — Normalize.** Use `reviewed snapshot` for the semantic source state and `snapshot ID` for its canonical identity. Environment-specific implementations may derive that ID from Git or another substrate without changing the concept.
2. **`state` overloaded for both source content and workflow progress — Normalize.** Use `reviewed snapshot` for source state and `workflow state` for review-process state.
3. **`provider`, `plug-in`, `integration`, and `backend` conflation — Normalize.** Use the functional definitions above so executable extension risk is not conflated with a remote/local service or persistence mechanism.
4. **`pass`, `stage`, `evaluation`, and `completion` used at incompatible levels — Normalize.** Keep canonical stage/pass terminology; reserve workflow `review completion` for the terminal program state and `completion eligibility` for deterministic transition eligibility.
5. **`passed`, `supported`, `complete`, `clear`, and `valid` risk semantic drift — Normalize.** Future schemas should define separate fields/enums by layer instead of relying on generic words. Existing historical records retain their historical vocabulary; migration must not rewrite them as though the new vocabulary existed earlier.
6. **Manual fallback treated as a special execution mode — Normalize.** A human semantic reviewer should satisfy the same provider-neutral semantic contract as model reviewers where substitution is claimed. `Manual fallback` describes availability/operation, not a different semantic authority class.
7. **Retrieval/indexing and exhaustive coverage risk conflation — Retain distinction.** Retrieval may assist review, while deterministic inventory/coverage evidence owns exhaustive accounting.
8. **Git/GitHub/repository terminology — Retain justified distinctions.** Git may be a local repository/versioning substrate; GitHub is a repository host; GitHub Actions is hosted execution. They must not be used interchangeably.
9. **History/event/evidence terminology — Normalize conceptually, defer representation.** `Occurrence` and `historical evidence` name the logical concepts; whether they are persisted as JSONL events, database rows, Git commits, or another form belongs to Structural Optimization.
10. **Evaluation terminology — Normalize without premature architecture choice.** Existing mapped items remain `evaluations` when discussing current behavior. Structural Optimization must decide whether the future workflow retains them independently or integrates them as visible stage acceptance criteria. The roadmap must not accidentally require both.
11. **Local correctness versus remote enforcement — Retain distinction.** These represent different authorities and threat models and should not be flattened into a generic `validation` concept.
12. **Breadth enforcement versus semantic correctness — Retain distinction.** Breadth evidence can prove required categories were accounted for structurally; it cannot prove the review was insightful or correct.

## Schema/design consequences handed forward

Structural Optimization and later implementation should prefer schemas that make the normalized distinctions explicit rather than encoding them only in prose. In particular:

- source identity fields should use one `snapshot_id` concept across inventory, indexes, semantic work packets, and evidence;
- workflow state and historical evidence should not share ambiguous `status` fields without typed context;
- provider adapters should expose capabilities through neutral contracts while executable plug-in enablement remains separately permissioned;
- semantic result fields and mechanical eligibility fields should be distinct;
- generated human-readable views should identify themselves as projections when they are not authoritative;
- historical migration should preserve old vocabulary/meaning or attach an explicit translation layer rather than silently normalizing old evidence in place;
- evaluation representation must have one visible workflow location after Structural Optimization decides its future form.

## Breadth check

Normalization was not limited to the user's newest requirements. The pass checked the full applicable normalization surface for the roadmap: workflow/state vocabulary, semantic/mechanical distinctions, provider/integration terminology, source/evidence identity, retrieval/coverage distinctions, review structure, local/host assurance, historical migration language, and evaluation representation. No material applicable normalization category was intentionally omitted.

Scope-inversion question: **What could remain materially inconsistent even if every stated user requirement were satisfied?** The main risks were semantic/mechanical status conflation, provider/plug-in/backend conflation, source-state/workflow-state conflation, evaluation/stage layering ambiguity, and migration vocabulary laundering. Those are addressed above.

## Handoff to Structural Optimization

Structural Optimization must now use these normalized concepts to choose the lowest-burden architecture. It should compare candidate state representations, decide whether Git is core or one substrate, decide whether the generated queue remains useful, decide the future representation of evaluations, minimize the provider/adapter surface, and determine the smallest local transaction/recovery model that still satisfies Adversarial and Interdependency requirements.

No implementation phase or pull-request breakdown is authoritative until Structural Optimization and End-to-end validation complete.
