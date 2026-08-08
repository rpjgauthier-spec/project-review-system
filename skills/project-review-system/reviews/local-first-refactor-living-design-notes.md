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

## Status

This document is intentionally unfinished. Continue appending/refining design decisions here during discussion. It is a design notebook, not evidence that the contained ideas have passed the Project Review System's governed semantic stages or implementation validation.
