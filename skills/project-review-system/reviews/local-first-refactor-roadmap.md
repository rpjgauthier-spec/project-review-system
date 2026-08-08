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
8. **Manual fallback:** the core workflow must remain usable when no local model, vector index, hosted model integration, or GitHub service is available, provided a human or other semantic reviewer can supply required judgments through the same bounded interfaces.
9. **Semantic/mechanical separation:** the LLM or human reviewer produces semantic judgments; deterministic software owns mechanically enforceable state and validation. Deterministic success must never be presented as proof that a semantic judgment is correct.
10. **Visible evaluation model:** mapped evaluations must either be explicit in the operating workflow or integrated into stage completion so they do not form a mostly hidden second review layer.
11. **Recoverability:** interrupted work, stale state, reopening, redo, rollback, migration, and historical evidence must have deterministic, comprehensible recovery paths.
12. **Low burden:** prefer the smallest architecture that preserves the required guarantees; do not preserve PR6-era complexity merely because it already exists.
13. **Assurance separation:** local validation may establish that the Project Review System's own review state and evidence satisfy its rules, but it must not claim to enforce a remote host's merge/branch policy. Preventing a privileged user from bypassing local checks is a repository-host control and may require optional host-side branch protection or CI. Core review correctness must not depend on that host enforcement.
14. **Atomic and concurrency-safe state:** a crash, interrupted write, second local process, stale client, or concurrent collaborator must not silently create two valid next states or partial authoritative state. The eventual state model must define atomic transition, compare-before-write, locking/conflict, and deterministic recovery behavior appropriate to supported platforms.
15. **Replay/identity safety:** whatever state representation is chosen must reject duplicated, reordered, replayed, forked, or same-logical-occurrence replacement evidence unless an explicit revision/reopening transition permits it. Do not rely on wall-clock timestamps as the ordering authority.
16. **Backward evidence preservation:** migration from the PR6-era records must preserve prior credited evidence and its identity without rewriting history to make the new architecture appear to have existed earlier. Old records may be read or transformed into a verifiable migration representation, but not silently re-authored.
17. **Untrusted-repository execution boundary:** scanning or reviewing a repository must not execute repository code, hooks, build scripts, tests, macros, or embedded instructions merely to inspect it. Symlinks, path traversal, archives, generated content, and hostile fixtures must not escape the authorized read/write scope.
18. **Plug-in installation boundary:** repository contents must not be able to auto-install, auto-enable, or silently select executable plug-ins. Plug-in code/configuration that can execute locally requires an explicit user-controlled trust/install decision, declared capabilities, and least privilege.
19. **Provider-data boundary:** provider configuration must make clear whether data stays local or may leave the machine. Sending repository content to a remote model/index/service requires an explicit configured provider path and must not occur merely because a local provider is unavailable.
20. **Sensitive-evidence minimization:** logs, histories, prompts, provider traces, and review artifacts must avoid storing secrets or unnecessary raw sensitive content. Evidence should retain the minimum references/hashes needed for traceability where full content is not required.
21. **Snapshot-bound retrieval:** semantic indexes and caches must identify the source snapshot they represent and fail stale rather than silently serving an old index as current evidence.
22. **Provider-output validation:** capability declarations and provider outputs are not trusted merely because they conform to an interface. Deterministic schema/range/snapshot checks must validate mechanically checkable claims before downstream use.
23. **Resource-bounded operation:** very large or malicious repositories must not require unbounded memory, recursion, archive expansion, context, or processing. Long-running deterministic work should be resumable where practical without converting partial work into completion credit.
24. **Portable ordinary use:** the reference implementation should avoid unnecessary dependence on one operating system, shell, hosted service, or filesystem behavior. Any unavoidable platform-specific guarantee must be explicit rather than silently assumed.
25. **Tamper-evidence boundary:** on a machine fully controlled by one user, the system cannot prove that the user did not rewrite all local state and history. The architecture may detect accidental corruption and make evidence tamper-evident, and may support stronger optional external/signed checkpoints, but must not claim impossible local non-repudiation.
26. **Human-operable failure mode:** if automation, retrieval, or models are unavailable, the system must expose enough current state, required inputs, conflicts, and next actions for a person to recover without reverse-engineering internal files.
27. **No bootstrap circularity:** implementing the new state engine must have a bounded migration/transition path that can be reviewed under the existing system without requiring the unfinished new engine to certify itself.
28. **Review-breadth enforcement:** for a declared full-program stage, user requirements, recent defects, and the proposed implementation are constraints and inputs, not implicit limits on the review lens. Stage completion must account for the complete applicable analysis surface defined by the canonical stage procedure, explicitly disposition non-applicable categories, answer what could still be materially wrong if every stated requirement were satisfied, and pass a breadth check against anchoring on recent prompts or defects. A materially narrow stage that receives completion credit is a false-credit defect and must be reopened. Deterministic tooling may enforce the presence and structure of this coverage evidence but must not claim to prove review quality.
29. **Canonical snapshot identity:** deterministic inventory, state transitions, retrieval/index caches, semantic packets, and completion evidence that claim to describe the same reviewed state must bind to one canonical snapshot identity produced by an explicit snapshot authority. Individual providers may not invent competing definitions of the current target.
30. **Provider-neutral semantic contracts:** human reviewers, local models, hosted models, retrieval systems, and alternate implementations must exchange bounded inputs and outputs through documented provider-neutral contracts where substitution is claimed. Manual fallback is not satisfied if internal state requires artifacts only a specific provider can produce.
31. **Workflow authority is separate from storage:** the workflow/state engine owns transition semantics, eligibility, logical occurrence identity, and validation rules. SQLite, files, an event log, Git, or another persistence backend may store that state but must not silently become a second workflow authority merely because its native behavior differs.
32. **User-owned provider permissions:** executable-provider enablement, capability grants, data-egress permission, and remote-provider fallback policy are controlled by explicit user configuration outside untrusted repository content. Provider self-description may advertise capabilities but cannot grant them.
33. **Collaboration conflict boundary:** when more than one clone/process/person can advance the same review, synchronization must detect divergent authoritative histories or stale bases and require deterministic reconciliation/reopening rather than silently accepting both as one valid lineage.
34. **Current-control transition completeness:** the refactor cannot claim local-first completion while canonical production rules still require GitHub Actions, branch protection, PR-specific evidence, or other hosted mechanisms for ordinary review correctness. The implementation plan must identify each current PR6-era control as retained locally, replaced, generated as an optional host integration, migrated, or deliberately removed with equivalent assurance.
35. **Single ownership for evaluation results:** until Normalization decides whether mapped evaluations remain independent or become stage acceptance criteria, each evaluation result must still have exactly one authoritative owner and stage/final advancement must consume it through one defined contract rather than duplicate it across reports, queues, and state views.

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

## Adversarial review

**Verdict: Complete.** Same-agent self-review; no independent-validation claim.

The pass attacked the roadmap as a whole rather than treating the user's requirements as the review boundary. The bounded claim is only that the roadmap now contains the constraints needed to prevent the identified architectural failure classes from being silently designed in; it is not a claim that an implementation already satisfies them.

### Blocking findings corrected in the roadmap

1. **Hosted-CI dependency / quota denial.** A required GitHub Actions path could make ordinary review unavailable when hosted quota or service is unavailable. The roadmap now requires zero hosted runs for normal operation.
2. **Remote-enforcement overclaim.** Local checks cannot prevent a privileged remote-repository user from bypassing local policy. Local review validity is separated from optional host merge/branch enforcement.
3. **Provider authority injection.** Retrieval/model/provider plug-ins could otherwise become accidental authorities or permission-expansion paths. Providers are least-privilege helpers with untrusted outputs by default.
4. **Stale retrieval/index poisoning.** A local semantic index can be internally consistent but bound to an old repository state. Retrieval/index caches must be snapshot-bound and fail stale.
5. **Plug-in supply-chain execution.** A reviewed repository could attempt to auto-select or install executable plug-ins, turning project data into local code execution. Plug-in installation/enabling is explicitly user-controlled and cannot be triggered by repository content.
6. **Repository-as-code execution.** A scanner that runs tests, hooks, macros, build scripts, archive extractors, or follows unsafe paths merely to inspect a project creates a local compromise path. Review inspection must be non-executing by default and bounded against path traversal, symlink escape, hostile archives, and embedded instructions.
7. **Partial-write and concurrency split-brain.** Transactional state was previously stated too generally. A crash or two writers could create multiple plausible next states. The roadmap now requires atomic transition, stale-write/conflict detection, and deterministic recovery semantics.
8. **Replay/forked-history false credit.** A naive event log or active/history split can duplicate, reorder, fork, or replay completion evidence. The state model must make logical occurrence identity and ordering deterministic and reject replacement without reopening/revision semantics.
9. **Migration evidence laundering.** A refactor could rewrite PR6-era history into the new schema and accidentally make new guarantees appear retroactive. Migration must preserve old evidence identity and distinguish historical format from new guarantees.
10. **Local tamper-proof overclaim.** A fully privileged local user can rewrite the program and its evidence. The system may provide tamper evidence and optional stronger checkpoints, but cannot claim local non-repudiation it cannot enforce.
11. **Provider-data leakage.** Automatic fallback from a local provider to a hosted provider could silently export repository content. Remote transfer must be explicit in configured provider selection; lack of a local provider cannot silently widen the trust boundary.
12. **Sensitive evidence retention.** Append-only history, provider traces, or prompts could permanently preserve credentials/private content. The roadmap now requires evidence minimization and redacted/reference-based traceability where full content is unnecessary.
13. **Resource-exhaustion denial.** Huge repositories, recursive structures, archives, or oversized semantic packets could make a supposedly local system unusable. Deterministic operations need bounded resources and resumable long work without partial-completion credit.
14. **Manual fallback that is only nominal.** If internal APIs require model/index-produced artifacts, "manual fallback" would be false. Human or alternate reviewers must be able to supply the same bounded semantic interfaces directly.
15. **Opaque deterministic overclaim.** Moving bookkeeping into code can make invalid semantic conclusions look stronger. Mechanical checks may establish consistency/eligibility only; they cannot certify semantic correctness.
16. **Dynamic subdivision boundary bypass.** Future mid-pass subdivision could otherwise rename/reframe work after it begins and evade the pass/history rules. Any future subdivision design must preserve prior state, ordering, identity, and exact downstream handoff rather than rewriting the original occurrence.
17. **Bootstrap circularity.** Requiring the unfinished new engine to validate the migration that creates it would make the refactor logically circular. The migration must be reviewable under the current merged system until the new engine is itself validated.
18. **Platform-assumption failure.** Local-first can still exclude ordinary users if correctness quietly depends on POSIX locking, shell behavior, case-sensitive paths, or GitHub-specific metadata. Platform-specific guarantees must be explicit; ordinary reference operation should avoid unnecessary platform coupling.

### Material attacks retained as explicit later-stage questions

These did not require choosing an implementation during Adversarial, but later stages must resolve them before the roadmap can become an implementation plan:

- Whether Git itself remains a required local substrate or should be one repository-storage provider. The current Project Review System is repository-based, so this is not assumed either way yet.
- Whether one append-only event log, split active/history files, SQLite, or another transactional store gives the lowest-burden reliable state model.
- How provider capability discovery works without trusting self-description or adding a plug-in framework larger than the review system.
- Which evidence needs full retained content versus hashes/references, especially when semantic reproducibility conflicts with sensitive-data minimization.
- Which cross-platform atomicity/locking guarantees the reference implementation can actually provide on Windows, macOS, and Linux.
- Whether optional signed or remote checkpoints add enough assurance to justify their complexity for users who want stronger tamper evidence.
- How much semantic preprocessing may be delegated to Phi or another local model before the stronger reviewer risks inheriting biased/omitted candidate sets.
- Whether the existing generated revalidation queue survives the refactor, becomes only a generated human-readable view, or disappears behind a simpler state projection.
- Whether mapped evaluations should remain independent checks, become stage acceptance criteria, or be represented through another visible mechanism.

### Non-blocking observations

- Command names such as `begin-pass`, `complete-pass`, `status`, and `resume` remain placeholders; naming is not an Adversarial blocker.
- LlamaIndex and Phi 14B are useful reference integrations but should not shape the generic interfaces prematurely.
- Optional hosted CI may still be useful for public collaboration or merge enforcement, provided the local workflow is complete without it.

### Adversarial completion boundary

No remaining identified defect within the accessible roadmap scope currently permits the roadmap itself to claim an unsafe guarantee, silently require hosted CI, make a plug-in/provider authoritative, or erase the need for atomicity, replay safety, migration integrity, data-boundary controls, manual recovery, breadth enforcement, and assurance limits. The implementation does not yet exist, so those requirements must be tested again against the concrete architecture and code later.

## Interdependency review

**Verdict: Complete.** Same-agent self-review; no independent-validation claim.

The pass mapped the material producers, consumers, authorities, fallbacks, and transition duties without selecting a persistence technology or implementation decomposition prematurely.

### Authority and dependency map

- **User/operator configuration authority:** owns provider installation/trust decisions, executable capability grants, data-egress permission, remote fallback policy, and any optional host-enforcement choice. Repository content and provider self-description are consumers/inputs only and cannot elevate those permissions.
- **Snapshot authority:** owns the canonical identity of the reviewed source state. Deterministic inventory, retrieval/index caches, semantic work packets, state transitions, and completion evidence consume this identity. A stale or mismatched snapshot blocks current-state credit.
- **Workflow/state engine:** owns current review state, allowed transitions, logical occurrence identity, revision/reopening semantics, mechanical completion eligibility, conflict detection, and deterministic status/resume projections. It consumes semantic judgments and deterministic evidence but does not own their semantic truth.
- **Persistence backend:** stores authoritative workflow events/state and historical evidence under the state engine's schema/transition rules. It may be files, SQLite, an event log, Git-backed storage, or another implementation. Native backend behavior is not a second workflow authority.
- **Deterministic inventory/validation layer:** produces mechanically checkable inventory, hashes, schema validation, coverage accounting, stale-state detection, replay/conflict checks, and bounded resource/error signals. The state engine consumes these results. Passing checks do not certify semantic correctness.
- **Semantic reviewer:** human, local model, hosted model, or another reviewer produces bounded semantic judgments/findings through provider-neutral contracts. The state engine records/consumes those judgments only when required mechanical prerequisites are satisfied.
- **Retrieval/index provider:** consumes a canonical snapshot plus bounded retrieval request and produces candidate context with snapshot/provenance metadata. It is optional, replaceable, and cannot define exhaustive scope or workflow authority.
- **Local/hosted model provider:** consumes bounded semantic packets and returns proposal/judgment payloads under the same provider-neutral contract where substitution is claimed. It has no repository/state permissions unless separately and explicitly granted for another role.
- **Evaluation result owner:** exactly one authoritative result per evaluation is recorded by the workflow state model. Stage/final advancement consumes that result once. Reports and human-readable status views reference/project it rather than re-own it. Normalization may later decide whether evaluations remain separate objects or become stage acceptance criteria.
- **History/archive:** preserves credited occurrences, revisions, migrations, and evidence references with identity/provenance. It is consumed for replay prevention, reopening, audit, and migration. It does not advance current state by itself.
- **Migration adapter:** consumes legacy PR6-era evidence and produces a distinguishable migrated representation or compatibility view. It cannot silently rewrite historical guarantees or certify itself with the unfinished new engine.
- **Collaboration/synchronization layer:** exchanges state between processes/clones/collaborators and must surface divergent lineage/stale bases to the state engine. It cannot silently merge two authoritative histories into one valid progression.
- **Repository host/GitHub integration:** optional consumer/publisher of locally valid state and optional provider of stronger remote merge enforcement. Host status does not become the source of truth for local review correctness.
- **Human-readable status/queue/report views:** generated consumers of authoritative state. They explain current state, missing inputs, conflicts, and next actions, but cannot independently advance or redefine the workflow.

### Material dependency findings corrected in the roadmap

1. **No single target-state owner.** Snapshot binding appeared in several requirements but no component owned the definition of current reviewed state. Added a canonical snapshot authority consumed by inventory, retrieval, semantic packets, state, and completion evidence.
2. **Provider substitution lacked a shared contract.** "Plug-and-play" and manual fallback would be nominal if each provider produced private shapes. Added provider-neutral semantic contracts so humans, Phi, ChatGPT, Claude, retrieval systems, or later providers can substitute where the capability is claimed.
3. **Storage risked becoming workflow authority.** Choosing SQLite/event-log/files first could accidentally let storage-native behavior define transition semantics. Added an explicit boundary: the state engine owns workflow meaning; persistence only stores it.
4. **Provider permissions had no unique owner.** Least privilege was required, but the producer of capability grants/egress permission was ambiguous. Added explicit user-owned provider configuration outside repository-controlled data.
5. **Multiple-clone collaboration was underdefined.** Local process locking does not solve two clones or collaborators advancing from the same base. Added a divergence/stale-base contract requiring reconciliation or reopening rather than silent lineage merge.
6. **Current hosted controls could survive unnoticed.** The merged production system currently describes GitHub Actions/branch protection as mandatory enforcement for Project Review System pull requests. A local-first refactor would be internally contradictory if it added local tools but left those canonical dependencies untouched. Added a transition-completeness requirement requiring every current PR6 control to be classified as retained locally, replaced, optional host integration, migrated, or deliberately removed with equivalent assurance.
7. **Evaluation ownership could remain duplicated.** Until the hidden-evaluation-layer design is normalized, the roadmap now requires one authoritative result owner and one consumption path, preventing reports/queues/state from becoming competing sources.
8. **Breadth enforcement needed a downstream implementation contract.** Added review-breadth enforcement as a core requirement: full-program stage completion must account for canonical analysis families, explicit N/A rationales, scope inversion, and anti-anchoring breadth evidence; deterministic tooling may enforce structure but not semantic quality.

### Required propagation and fallback contracts

- A **source snapshot change** invalidates or stales any current retrieval cache, semantic packet, gate/transition evidence, or completion claim bound to the previous snapshot unless its role is explicitly historical.
- A **provider unavailable/failing** condition falls back to another explicitly configured compatible provider or manual semantic input; it must not silently expand permissions or export data remotely.
- A **provider output schema/snapshot mismatch** is rejected before semantic or state consumption; the fallback is retry/alternate provider/manual input, not coercion into the expected shape.
- A **state write conflict or divergence** blocks advancement and exposes competing bases/lineages for deterministic reconciliation or explicit reopening.
- A **persistence failure** must leave either the prior authoritative state or one committed next state, never a partially authoritative intermediate state.
- A **migration failure** leaves legacy evidence readable under the old authority path and does not partially convert it into current guarantees.
- A **missing retrieval/index service** must not block ordinary/manual review; only capabilities explicitly requiring semantic retrieval become unavailable.
- A **remote host unavailable/quota exhausted** does not block local review progression or completion; only optional host collaboration/enforcement is unavailable.
- A **generated status/report disagreement** is resolved in favor of authoritative state and treated as a stale/generated-view defect, not as permission to advance from the report.
- A **breadth-accounting omission** blocks full-program stage completion structurally; a passing breadth structure still does not prove the substantive review was adequate.

### Current-control transition inventory required before implementation completion

The implementation plan must explicitly account for at least these current control families rather than assuming the refactor automatically supersedes them:

- Adaptive Execution gate creation and completion evidence;
- pass-boundary/handoff chronology;
- review revision/reopening rules;
- occurrence identity/history and replay protection;
- artifact/current-state binding;
- change-impact records and class-to-stage/evaluation mapping;
- generated revalidation queue and final completion gate;
- changed-file coverage enforcement;
- regression and structural validators;
- Git/GitHub-specific exhaustive inventory controls where Git is the evidence model;
- GitHub Actions/branch-protection enforcement as an optional host layer rather than ordinary local-review authority;
- legacy/historical evidence and migration semantics.

### Interdependency completion boundary

Within the roadmap's accessible scope, every material proposed role now has a bounded authority/producer/consumer relationship, major fallback paths are identified, and the current production controls have an explicit transition-accounting obligation. The stage deliberately does not choose Git versus non-Git snapshots, SQLite versus files/event log, or separate versus stage-integrated evaluations; those are terminology/structure choices for Normalization and Structural Optimization so long as the ownership contracts above are preserved.

## Reviewer independence

Same-agent self-review. This review may improve the design but is not independent validation.

## Current review state

- Adversarial: Complete
- Interdependency: Complete
- Normalization: Ready
- Structural Optimization: Pending
- End-to-end validation: Pending

## Next bounded handoff

Normalization must resolve ambiguous or overlapping concepts before architecture selection, especially snapshot/target identity, state versus evidence versus generated views, provider versus capability versus adapter, evaluation versus stage acceptance criteria, completion versus eligibility versus host enforcement, review breadth versus exhaustive semantic coverage, and migration/legacy terminology. It must retain the authority and propagation boundaries established by Interdependency.

No implementation phase or pull-request breakdown is authoritative until the five-stage review completes.
