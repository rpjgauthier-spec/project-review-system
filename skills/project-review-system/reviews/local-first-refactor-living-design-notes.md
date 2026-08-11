# Local-First Refactor Living Design Notes

## Purpose

This is a living, non-authoritative design-notes document for the Project Review System local-first refactor. It exists so implementation refinements, dogfooding findings, alternative architectures, and future review-method improvements can be accumulated without silently changing the already-reviewed roadmap target.

The reviewed roadmap and current validated Project Review System remain authoritative until an explicit validated cutover. Material changes discovered here must later be classified and, when they change authority, lifecycle, protected controls, or reviewed behavior, routed through the appropriate bounded reopening/review path rather than being treated as retroactive approval.

## Current architectural direction

Core split:

- LLM/human reviewers own semantic judgment.
- Deterministic software owns state transitions, hashes, validation, persistence, recovery, orchestration order, and derived projections.
- No required Project Review System capability may depend on GitHub Actions or hosted CI quota.
- Git/GitHub are optional adapters/observability layers, not core correctness authorities.
- Provider integrations are replaceable capability interfaces; no specific provider is required for core correctness.

## Implementation refinements from external critique

### Transactional pass lifecycle

Treat lifecycle setup, deterministic calculations, validation, and durable completion as one architectural unit rather than separate independently deployed designs.

Preferred implementation sequence:

1. define exact `begin-pass` / semantic-result / `complete-pass` contracts;
2. implement deterministic `begin-pass`;
3. implement transactional `complete-pass`;
4. move all hashes, revision arithmetic, state-machine transitions, gate derivation, queue/projection updates, and persistence bookkeeping into the controller.

The semantic reviewer should not calculate or mutate state-machine internals.

### Minimal semantic result interface

Keep the semantic reviewer output intentionally small. Conceptually:

```json
{
  "stage": "Normalization",
  "verdict": "supported",
  "findings": [],
  "unresolved_conditions": [],
  "evidence_refs": []
}
```

The controller derives hashes, occurrence identity, revision relationships, next valid action, completion eligibility, queue/projection state, and persistence operations.

### Defer physical history decomposition

Do not prematurely commit to a specific split such as `active.json`, `occurrences.jsonl`, and `revisions.jsonl` merely because it is plausible.

The actual requirement is:

> Keep frequently-read authoritative current state small while preserving durable immutable history and replay/recovery evidence.

Choose the physical storage/schema split only after access patterns, validation needs, retention, concurrency, and migration behavior justify it. SQLite remains the current reference persistence direction, but the architectural contract should remain persistence-neutral where practical.

### Narrow status and recovery commands

Avoid a generic `resume` command becoming a second ambiguous orchestrator.

Preferred concepts:

- `status`: read-only report of authoritative durable state and next valid action;
- `repair`: deterministic, idempotent maintenance only; never performs semantic work and never advances semantic stage credit;
- `begin-pass <stage>`: creates/reuses the one valid occurrence/gate for the current state;
- `complete-pass <stage> <semantic-result>`: validates and atomically records one semantic completion.

### Idempotency as a first-class requirement

Where practical, deterministic operations should be idempotent.

Examples:

- repeating `begin-pass Normalization` against the same valid state should return the already-existing occurrence/gate or fail cleanly because the state has advanced; it must not create an equivalent duplicate gate;
- retrying `complete-pass` after an interruption should deterministically return `already completed` when the exact logical occurrence is already durably complete;
- retrying projection/repair operations must not create duplicate history or change semantic credit.

Idempotency complements atomic persistence and directly reduces interruption/recovery ambiguity.

### Persistence-neutral atomicity

Core correctness requires one atomic durable authoritative state transition. A Git commit is optional adapter-level evidence/observability, not the state authority itself.

When a Git adapter is active, repository updates and durable Git observability should be coordinated so interruption cannot create false semantic credit or an apparently current projection that disagrees with authoritative state.

## Dogfooding findings that must inform the redesign

### Generated projections became stale

Observed failure: the committed/generated revalidation queue became stale after authoritative state/evaluation mutations and required separate synchronization bookkeeping.

Redesign requirement:

- status, queue, preflight, and similar projections should either derive on demand directly from authoritative state or update atomically as part of the authoritative transition;
- a stale generated view must never masquerade as current authority;
- freshness must be mechanically checkable;
- normal one-evaluation-at-a-time operation should not require a second manual bookkeeping commit only to synchronize a derived view.

Related public issue: #8, `Refactor: make generated review projections self-synchronizing`.

### Whole-file authoritative mutation was fragile

Observed failure: adding one evaluation result through a whole-file replacement accidentally altered one character of unrelated immutable End-to-end handoff evidence before a repair commit restored it.

Redesign requirement:

- authoritative mutations must be narrow and transactional;
- recording one result must not require retranscribing or replacing unrelated immutable evidence;
- state-transition APIs/database operations should update only intended fields and verify invariant preservation;
- immutable occurrence evidence should be append-only or otherwise protected from incidental mutation.

### User-visible durable pass identity

For Git-backed operation, user-facing governed semantic-pass responses should surface the Git commit SHA that first durably records that pass's credit/completion.

This is observability and chronology evidence, not a replacement for execution-unit identity, boundary identity, gate identity, handoff chaining, target-state binding, or deterministic history checks.

### Durable pass finalization must be fail-closed

Observed failure during artifact-identity dogfooding: a semantic Adversarial pass was completed and its completion/handoff evidence was calculated, but the execution unit terminated before that evidence was durably written. The semantic work was recoverable from transient context, but the authoritative repository contained no completed occurrence for the pass.

This was an agent/operator execution error, but it exposed a deterministic lifecycle gap. The system already validates completed-pass chronology, handoff chaining, gate identity, target-state binding, and immutable occurrence evidence after those artifacts exist. It does not yet make **durable persistence a prerequisite for pass termination**.

Redesign requirement:

> A semantic pass is not complete when semantic judgment finishes. It is complete only after the controller has validated and atomically persisted the exact completion/handoff for the current occurrence and can read back that durable state.

Preferred lifecycle:

```text
semantic pass executes
        ↓
semantic findings/verdict complete
        ↓
construct semantic-result payload
        ↓
controller validates current gate / revision / target / pass identity
        ↓
atomically persist completion + handoff + occurrence history
        ↓
read back / verify durable authoritative state
        ↓
ONLY NOW may the execution unit report pass completion
```

Fail-closed behavior:

- if semantic work finishes but durable completion has not been persisted, authoritative pass status remains `INCOMPLETE`;
- no later semantic stage may consume the transient result as prior-stage credit;
- retrying `complete-pass` after interruption must be idempotent: exact already-durable completion returns `already completed`; incomplete persistence resumes or retries without creating a second logical occurrence;
- the controller should expose a mechanically checkable finalization predicate such as: current gate exists, exact completion exists, completion validates against the gate/target/revision, and authoritative persistence confirms the occurrence;
- when a Git observability adapter is enabled, the user-facing pass response should not claim durable Git completion until the corresponding commit is confirmed, but Git remains adapter evidence rather than the core state authority;
- transient model context, scratch files, computed hashes, or a user-visible statement that the pass is done are never substitutes for durable authoritative completion.

This should be implemented as part of transactional `complete-pass`, not as a new semantic review layer or a separate optional housekeeping command. The normal success path should make it difficult to express the invalid intermediate state “semantic pass finished; persistence still pending.”

Host limitation: repository/controller logic cannot literally prevent an external chat host from ending a message or losing a model context. It can, however, ensure that such an interrupted execution remains mechanically **non-creditable and incomplete**, so lost transient work cannot masquerade as a completed governed pass.

### Bounded multi-finding semantic passes

Observed failure mode during controller-core dogfooding: Adversarial review repeatedly stopped after the first blocker, causing a sequence of correction revisions in which the next independently discoverable blocker appeared only after the prior one was fixed. This preserved fail-fast semantics but created unnecessary revision churn and repeated review setup.

The redesign should distinguish **stage failure** from **investigation termination**.

Preferred behavior:

- a semantic stage may be subdivided into bounded, predeclared review subpasses when one monolithic pass would either overload reviewer context or encourage first-defect termination;
- each subpass should have a narrow declared scope and may record all findings discoverable within that scope rather than stopping after its first blocker;
- a blocking finding in an earlier subpass does not by itself cancel later subpasses in the same already-authorized stage plan;
- findings and unresolved conditions are handed forward durably between subpasses using the normal execution-unit, boundary, handoff, target-state, and chronology controls;
- later semantic stages remain blocked unless the enclosing stage ultimately receives passing credit;
- the enclosing stage receives PASS/FAIL only after the required subpass plan is complete, so the aggregate result can contain the full blocker set discovered by the bounded sweep;
- correction/reopening rules remain unchanged after aggregate failure.

This should reuse the ordinary subdivided execution mechanism rather than introduce a second "multi-problem review" authority. Existing safeguards such as declared pass order, unique execution identities, exact handoff consumption, durable pass chronology, and full-plan completion before stage credit should remain mandatory.

Context pressure is a governing constraint. Subdivision should be adaptive: use several small review areas instead of asking one reviewer context to retain the whole stage when doing so risks context degradation. Individual subpasses may require stronger isolation where semantics justify it, while ordinary bounded subpasses can remain separated.

A practical Adversarial decomposition for a small controller/domain slice might include scopes such as:

- runtime/type and construction invariants;
- cross-field and cross-object authority invariants;
- frozen-contract completeness and representability;
- persistence, retry, and immutable-evidence boundaries;
- final integrated adversarial sweep.

The exact decomposition should be selected from the governed target, not hard-coded globally.

Open questions for redesign:

- When should a blocker terminate only its current subpass versus the entire stage investigation?
- What conditions make continued investigation invalid or unsafe, such as unreadable/corrupt authoritative input?
- Should the controller require an explicit aggregate stage-result artifact after the final subpass, or derive the aggregate result from the completed subpass handoffs?
- How should subpass sizing adapt to model context limits without letting context-window heuristics become semantic authority?
- What minimum evidence should prove that a multi-finding sweep was complete enough to justify correction of several blockers in one revision?

## Cross-stage de-anchoring / solution-space exploration

A major review-method gap was discovered after an external AI immediately identified simplifications that the dogfooded review did not surface.

The problem was not limited to Structural Optimization. Adversarial, Interdependency, Normalization, Structural Optimization, and End-to-end validation can all contribute to proposal anchoring if the proposed decomposition is treated as the default solution.

### Review-wide rule

A full-program review must not treat the proposed architecture, phases, artifacts, commands, interfaces, persistence layout, or workflow decomposition as the default solution merely because they were supplied by the proposer.

Relevant stages must challenge those boundaries against requirements and invariants. “The proposal is coherent” is not sufficient evidence that the structure is justified.

### Stage-specific responsibilities

- **Adversarial:** attack inherited assumptions; identify simpler or materially different designs that could invalidate the proposal.
- **Interdependency:** test whether proposed boundaries create duplicate authorities, circular control, unnecessary coupling, or ambiguous orchestration.
- **Normalization:** determine whether apparent architectural differences are only terminology/history artifacts or represent real semantic distinctions.
- **Structural Optimization:** reconstruct and compress the architecture; attempt to merge/remove every phase, command, persistent artifact, authority, and interface unless a distinct invariant/lifecycle/consumer/security/failure-mode reason requires separation.
- **End-to-end validation:** trace sufficiently different/simpler alternatives far enough to verify that rejected complexity is actually necessary rather than merely familiar.

### Avoid self-attestation

Do not rely on a question such as:

> Would the reviewer independently arrive at substantially the same architecture?

A model can answer “yes” without demonstrating anything.

Instead require a comparative process with durable artifacts.

## Independent solution-space exploration followed by adversarial convergence

For substantial architectural reviews, one reconstruction may still anchor on one arbitrary alternative. Prefer multiple materially distinct candidates when the solution space supports them.

### Divergence phase

Before showing the original proposal, provide reviewers only a requirements packet containing the governing requirements, invariants, constraints, known failure modes, external interfaces, and relevant protected controls.

Generate multiple candidate architectures independently. Material difference should involve meaningful differences in authority boundaries, persistence strategy, orchestration shape, decomposition, interfaces, or failure/recovery behavior rather than renaming the same graph.

### Cross-critique phase

After candidates are frozen, expose them to one another for critique. Useful tasks include:

- identify unjustified complexity in another candidate;
- identify controls or failure paths another candidate misses;
- identify assumptions shared by all candidates that may not follow from the requirements;
- identify components that can be merged or removed;
- identify disagreements that are merely terminology.

### Normalization before convergence

Normalize equivalent concepts before treating differences as substantive. For example, `event log`, `immutable occurrence ledger`, and `append-only history` may represent the same architectural role.

### Reveal the original proposal last

Only after independent candidates and cross-critiques are frozen should the original proposal become visible to the comparison step.

Then record:

- proposal elements independently rediscovered;
- proposal-only elements;
- candidate-only elements;
- different boundaries;
- simpler alternatives;
- justification for every retained proposal-only component or boundary;
- recommended architecture and rejected alternatives with reasons.

A proposal-only element should not be retained merely because it already exists. It needs a distinct invariant, lifecycle, consumer, authority boundary, security boundary, or failure mode that justifies separation.

## Multi-reviewer / multi-model option

The Project Review System should support stronger optional assurance by allowing multiple reviewer providers/models to generate independent candidates.

Possible configurations include:

- same model in multiple isolated fresh contexts;
- different models from the same provider;
- different model families/providers;
- local models plus hosted models;
- models plus independent human/domain expert review.

These are not equivalent assurance levels. The system should record provenance/independence metadata rather than claiming they provide the same independence.

Example conceptual metadata:

```json
{
  "candidate_id": "candidate-b",
  "reviewer": {
    "provider": "local",
    "model": "phi-14b",
    "independence_group": "solution-space-2"
  },
  "input_snapshot": "requirements-packet-sha256:...",
  "proposal_visible": false
}
```

The deterministic controller can verify process facts such as same requirements snapshot, distinct execution slots/contexts, proposal visibility state, output immutability, and chronology. It cannot prove the semantic quality or true cognitive independence of a model.

Consensus should increase confidence, while disagreement should create focused adversarial work. Do not treat majority vote as proof.

## Hierarchical draft-and-converge topology

An additional optional topology is to use several cheaper/local models as parallel draft generators, then use a stronger primary model to refine each draft separately. Each branch remains independent and becomes its own converged candidate document before cross-branch comparison.

Conceptually:

```text
requirements-only packet
        │
   ┌────┼────┐
   │    │    │
 local A local B local C
   │    │    │
 rough A rough B rough C
   │    │    │
   └─ primary model refines each branch separately ─┘
            │       │       │
        refined A refined B refined C
            │       │       │
       local↔primary bounded critique loops
            │       │       │
       converged A converged B converged C
            └───────┼───────┘
                    │
        compare converged documents
                    │
        disagreements / synthesis / selection
```

### Why this may be useful

- local models cheaply increase solution-space breadth;
- a stronger primary model can repair weak prose, missing reasoning, and incomplete architectural articulation without collapsing every branch into one design immediately;
- back-and-forth critique can force each branch to defend and improve itself;
- several independently converged documents provide a stronger comparison set than several raw first drafts;
- semantic disagreements that survive repeated critique become more informative because easy mistakes and wording differences have already been reduced.

### Preserve branch independence during refinement

The primary model should refine candidate A without seeing B/C during A's branch-convergence loop, and likewise for the other branches. Otherwise the primary model can prematurely homogenize the candidates.

Each branch should bind to:

- the same requirements snapshot;
- its original rough-draft hash;
- every critique/refinement occurrence in order;
- reviewer/model provenance for every turn;
- a branch identity that remains stable through convergence;
- proposal visibility state.

Only after branch convergence/freeze should the controller permit cross-branch comparison.

### Ephemeral branch execution and parent-context firewall

Branch independence does not necessarily require separate persistent chats. A stronger and lower-burden option is to let the primary model perform a rich local↔primary refinement loop inside one bounded execution while strictly limiting what is allowed to cross back into the parent conversation.

Conceptually:

```text
Parent conversation
    │
    ├─ execute Branch A
    │      requirements + rough A
    │      primary ↔ local A
    │      primary ↔ local A
    │      primary ↔ local A
    │      ↓
    │   candidate-A stored durably
    │      ↓
    │   branch scratch/context discarded
    │      ↓
    └─ parent receives only: "Branch A complete"

Next parent turn
    │
    ├─ execute Branch B
    │      requirements + rough B
    │      no candidate-A content or A critique history
    │      ...
```

The substantive A refinement dialogue is therefore not part of the conversational context used to refine B. The parent conversation may retain only minimal metadata that A occurred, not what A proposed, what arguments were persuasive, what architecture the primary model preferred, what terminology was used, or how many rounds were needed.

The branch may still persist the mature candidate and audit/provenance data outside the parent context. Those artifacts remain unavailable to other independent branches until the workflow explicitly enters cross-branch comparison.

This creates a **lossy context boundary**:

- rich branch-local working context exists temporarily;
- the mature candidate is written to durable external state;
- the parent receives only a tiny completion receipt;
- intermediate branch dialogue/reasoning is discarded from subsequent independent branch context;
- the comparison phase later loads the frozen mature candidates intentionally.

A conceptual parent-return contract could be as small as:

```json
{
  "branch_id": "A",
  "status": "complete",
  "candidate_ref": "sha256:..."
}
```

For maximum isolation, the user-visible parent message could omit even the candidate reference and simply render `Branch A complete`; the deterministic controller keeps the durable reference internally.

### Branch context firewall requirement

The redesign should explicitly require a context firewall rather than trusting the primary model to merely avoid mentioning earlier branches:

> After an independent branch execution completes, substantive branch inputs, intermediate dialogue, critiques, reasoning, and candidate content must not be automatically supplied to subsequent independent branch executions. Only the explicitly declared parent-return payload may cross the branch boundary. Durable branch candidate artifacts remain inaccessible to other branches until workflow state explicitly authorizes cross-branch comparison.

This requirement is meaningful only if the execution environment actually discards or withholds branch scratch/context. Merely printing a short response while silently carrying the full hidden branch transcript into later model invocations does not provide isolation.

The deterministic controller should therefore distinguish:

- **branch scratch/context** — temporary and non-propagating;
- **durable candidate artifact** — retained but access-controlled by workflow phase;
- **parent-return payload** — intentionally tiny and allowed into the parent context;
- **comparison input** — explicitly assembled later from frozen candidates.

This topology also reduces context-window pressure: very large branch refinement dialogues can be discarded while only the mature candidate documents are retained for eventual comparison.

### Bounded local↔primary dialogue

A branch can alternate between the primary model and the local model that originated it. Example:

1. local model produces rough architecture;
2. primary model identifies defects and produces a refined version or structured critique;
3. local model responds to the critique, defending or revising its distinctive choices;
4. primary model re-evaluates the response and updates the candidate;
5. continue until a deterministic stopping condition is reached.

The objective is not unlimited debate. The controller should enforce a bounded convergence policy, such as a maximum number of rounds plus semantic stop outcomes like `no_material_change`, `unresolved_disagreement`, or `candidate_rejected`.

### Avoid primary-model collapse

A major risk is that the stronger primary model rewrites every branch into its preferred architecture. The protocol should therefore distinguish **refinement** from **replacement**.

During branch convergence, the primary model should be required to preserve the branch's defensible distinctive choices unless it records why a choice violates a requirement/invariant or is dominated by a simpler alternative. Material architectural changes should be explicitly listed rather than hidden inside prose rewriting.

The controller can mechanically require fields such as:

```json
{
  "branch_id": "candidate-b",
  "round": 2,
  "material_changes": [],
  "retained_distinctive_choices": [],
  "rejected_choices": [],
  "unresolved_disagreements": []
}
```

It cannot judge whether the primary model preserved diversity honestly, but it can make silent homogenization visible and reviewable.

### Compare converged documents, not only final recommendations

Do not immediately synthesize the branches into one document. Freeze the converged branch documents first and compare them as separate alternatives.

The comparison should identify:

- architecture shared by all converged branches;
- choices supported by only some branches;
- disagreements that survived critique;
- branches that converged only semantically/terminologically versus structurally;
- assumptions shared by all branches;
- components/boundaries that one branch eliminated successfully;
- reasons a minority branch may still be superior on a specific invariant or failure mode.

Only after this comparison should a final synthesis or selection occur.

### Optional nested diversity

The same topology can be expanded without changing the controller model. For example, two or more local models could seed each branch, or different strong models could independently refine different branches. The controller should model this as reviewer assignments to immutable jobs/branches rather than hard-coding a particular model hierarchy.

### Cost and assurance role

This topology can use local models for high-volume drafting/critique and reserve the strongest/most expensive model for refinement and cross-candidate judgment. It therefore offers a way to spend scarce high-capability model usage on the parts where it has the most leverage while still producing multiple competing design trajectories.

It is an optional assurance/performance topology, not a requirement for core Project Review System correctness.

## Deterministic orchestration of independent reviewers

Deterministic software and files can enforce the review protocol even though semantic work is external.

A simple conceptual artifact flow:

```text
requirements-only packet
        ↓
candidate A   candidate B   candidate C
        ↓          ↓          ↓
      frozen immutable candidate outputs
                 ↓
             cross-critiques
                 ↓
             normalization
                 ↓
          original proposal revealed
                 ↓
      proposal-vs-alternatives comparison
                 ↓
 selected architecture + rejected alternatives + reasons
```

The controller should own:

- job IDs and lifecycle;
- exact input hashes;
- proposal visibility state;
- allowed ordering;
- response schema validation;
- immutable/frozen candidate outputs;
- duplicate/retry handling;
- stale input rejection;
- provenance metadata;
- derived next action/status.

The controller should reject invalid process states such as:

- candidate generated after proposal reveal;
- candidate accidentally receiving another candidate during the independent generation phase;
- mismatched requirements hashes;
- overwritten frozen candidate files;
- critique occurring before candidate freeze;
- final proposal comparison occurring before required normalization/critique work;
- duplicate completion of the same logical job;
- stale response against an older requirements packet.

## Transport/provider tiers

Pure deterministic files cannot independently invoke unrelated hosted AIs without some callable interface. Without provider integration, the user becomes the transport layer by copying packets to a reviewer and importing the response.

The intended architecture should therefore distinguish transport from orchestration.

### Tier 1 — manual handoff fallback

The controller writes a request packet. A user manually gives it to an AI/human and imports the resulting response.

This is useful as a universal fallback and for occasional high-assurance reviews, but it should not be the intended normal experience.

### Tier 2 — local reviewer adapters

Local models can be invoked automatically through replaceable adapters, for example an OpenAI-compatible local endpoint, Ollama, llama.cpp server, vLLM, or another local inference interface.

The controller can run several isolated contexts of the same local model or multiple local models without manual copying after setup.

### Tier 3 — hosted reviewer adapters

Hosted models require a callable provider interface such as an API or another explicitly authorized connector. The adapter sends one bounded job and returns one bounded response.

Provider adapters must remain transport/capability implementations rather than orchestration authorities.

Conceptually:

```text
controller -> reviewer.execute(job) -> response
```

The controller owns sequencing, independence rules, hashes, retries, validation, and persistence. The adapter should be as dumb as practical: send this bounded request to this configured reviewer and return the response.

### Provider independence

The Project Review System core must not embed provider-specific orchestration logic throughout the state engine. Replaceable reviewer interfaces should allow configurations such as:

- local Phi + OpenAI + Claude;
- local Llama + Gemini + another future provider;
- local-only reviewers;
- hosted-only reviewers;
- human/manual fallback.

Changing providers must not change review semantics or state-machine authority.

## Candidate deterministic file protocol

A first implementation can use simple files even before automatic provider adapters exist.

Conceptual layout:

```text
review/
  requirements/
    packet.json
  candidates/
    candidate-a/
      request.json
      response.json
    candidate-b/
      request.json
      response.json
    candidate-c/
      request.json
      response.json
  critiques/
    ...
  normalized/
    comparison.json
  proposal/
    proposal.json
  final/
    proposal-comparison.json
```

Every artifact should bind to exact input hashes and job identity. The physical layout is illustrative, not yet an architectural commitment; the implementation may instead represent these entities transactionally in SQLite with generated/exported files.

## Open design questions to continue refining

- What review size/risk threshold should trigger multiple independent candidate designs?
- What is the minimum useful candidate count, and when should the controller allow fewer because the solution space genuinely does not support several materially distinct designs?
- How should fake diversity be detected without pretending deterministic software can judge architecture quality?
- How should reviewer independence/assurance levels be represented without overclaiming?
- Which cross-critiques should be mandatory versus adaptive?
- Should proposal reveal be an explicit durable state transition?
- Which semantic-result fields are truly necessary for candidate generation, critique, normalization, and final comparison?
- How should local provider isolation and optional network-isolation claims be represented and verified?
- How should user-visible Git commit SHA observability interact with a persistence-neutral local state engine?
- What exact conditions should allow deterministic `repair` to modify state without triggering semantic reopening?
- How should the current validated Project Review System govern migration/cutover into this redesigned controller without circular self-certification?
- What deterministic stopping rule should govern local↔primary convergence loops?
- How should the system detect when a primary model is collapsing nominally independent branches into one architecture?
- When should converged minority designs be preserved for final comparison rather than eliminated during branch refinement?
- What execution-environment guarantees are required to prove that ephemeral branch scratch/context is not propagated into later independent branches?
- What is the minimum parent-return payload needed to resume orchestration without leaking substantive branch content?

## Status

This document is intentionally unfinished. Continue appending/refining design decisions here during discussion. It is a design notebook, not evidence that the contained ideas have passed the Project Review System's governed semantic stages or implementation validation.