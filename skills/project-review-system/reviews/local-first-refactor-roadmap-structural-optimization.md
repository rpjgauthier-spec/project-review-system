# Local-first refactor roadmap — Structural Optimization review

## Scope

Structural Optimization of the post-PR6 refactor roadmap after completed Adversarial, Interdependency, and Normalization review. This stage selects the lowest-burden reliable architecture while preserving the established authority, safety, evidence, recoverability, portability, provider, breadth, and migration requirements.

## Verdict

**Complete.** Same-agent self-review; no independent-validation claim.

The architecture below is the selected roadmap architecture for End-to-end validation. It is still a design, not an implemented guarantee.

## Selected minimal architecture

### 1. One local workflow engine

Use one deterministic local workflow engine as the sole authority for review transitions, revision/reopening rules, logical occurrence identity, stage/pass ordering, completion eligibility, stale-state/conflict handling, and current status/resume projections.

Do not preserve separate scripts as independent state authorities. Existing validators may survive as internal modules or commands, but they consume the same state engine and normalized contracts.

The semantic reviewer remains separate: human or model supplies semantic results; the workflow engine can validate their shape, snapshot binding, required coverage evidence, and transition eligibility but cannot certify semantic truth.

### 2. SQLite as the reference local persistence backend

Use Python's standard-library SQLite as the reference persistence backend for new workflow state and history.

Why selected over the main alternatives:

- **Split JSON/JSONL files:** easy to inspect and Git-diff, but cross-file atomicity, locking, stale-write prevention, indexing, and crash recovery recreate much of the complexity PR #6 accumulated.
- **One append-only JSONL event log:** attractive conceptually, but safe concurrent append, partial-line recovery, indexing/projection, migration, and cross-platform locking still require a database-like layer.
- **Multiple active/history files:** rejected because it creates synchronization and partial-write surfaces without providing a compensating benefit.
- **SQLite:** provides transactions, locking, integrity constraints, indexing, and crash-safe local commits using the Python standard library and no hosted service.

The logical model should remain event/evidence oriented: immutable credited occurrences and transition history are retained; current workflow state is a projection/materialized state derived under the same transaction rules. The exact SQL schema is an implementation design task and should not be frozen by this roadmap.

SQLite is a persistence mechanism, not the semantic/workflow authority.

### 3. Do not use the SQLite file itself as a collaboration merge artifact

A SQLite database is local authoritative storage for one review lineage, not a file that collaborators attempt to text-merge through Git.

For collaboration or machine transfer, define a deterministic **portable review bundle** export/import boundary containing the required normalized events/evidence, lineage/base identity, schema version, snapshot IDs, and integrity information. Import must detect stale/divergent lineage and reject silent combination. Reconciliation/reopening is explicit.

Do not build real-time multi-user synchronization in the first refactor. That would be disproportionate to the current need.

### 4. Git remains the default repository/snapshot adapter, not the semantic core

Do not require GitHub or GitHub Actions for core correctness.

For the first implementation, keep Git as the default supported repository/snapshot adapter because the current Project Review System is repository-based and already relies heavily on Git object/diff evidence. Separate the normalized snapshot interface from Git-specific evidence so the semantic/state engine does not depend on Git terminology internally.

Do **not** build a broad multi-VCS framework now. Define the small snapshot/inventory adapter boundary and ship the Git implementation. A filesystem or other repository adapter can be added when there is a concrete consumer.

This preserves current functionality without mistaking GitHub for Git or prematurely generalizing to every storage system.

### 5. Replace the committed revalidation queue with a generated projection

The current generated `reviews/revalidation-queue.md` should not remain a committed mutable coordination artifact in the new workflow.

The state engine should derive required stages, evaluations/criteria, unresolved work, and final completion eligibility directly from authoritative state plus the canonical revalidation mapping. `status`/`plan` can render this as terminal text, JSON, or optional Markdown.

A generated Markdown queue may remain as an export for humans or compatibility, but it is a projection and is not committed/edited as part of normal operation.

This removes queue source-hash churn, stale generated-file commits, and a substantial portion of PR6 bookkeeping.

### 6. Keep the canonical five stages; integrate mapped evaluations into the visible stage work plan

Do not retain a mostly hidden second workflow layer of evaluations that appears after the five stages.

Keep evaluation definitions as reusable semantic acceptance checks where they add distinct coverage, but the workflow engine should place every required evaluation into the **visible work plan from the start** and assign it to an owning stage or explicit final cross-stage criterion through the canonical mapping/configuration.

Rules:

- an evaluation has one result owner;
- it is visible before the stage that owns it begins;
- stage completion includes its owned required criteria when applicable;
- genuinely cross-stage/final criteria remain explicitly visible as final criteria rather than being disguised as a sixth stage;
- the user-facing workflow still remains the five canonical semantic stages.

Do not duplicate the same evaluation as both an independent hidden result and a second stage acceptance result.

The exact ownership assignment belongs in implementation/mapping design, but hidden post-stage evaluation work is rejected.

### 7. Integrate breadth accounting into each full-program stage contract

Add a small canonical structured stage-contract definition for mechanically required breadth categories. The stage semantic module remains the prose authority for what those categories mean; the structured contract exists only so the workflow engine can require an accounted-for result or explicit N/A rationale for each applicable category.

Also require the scope-inversion answer and anti-anchoring breadth assertion before full-program stage completion.

Do not create a separate breadth-review stage or permanent reviewer role. Breadth is a completion criterion of the existing stage.

A structurally complete breadth record does not prove semantic quality.

### 8. Thin provider adapters, not a large plug-in framework

The core should define a small provider-neutral request/response contract and capability manifest.

Preferred integration surface:

- built-in/manual semantic input is always available;
- external adapters may be configured as local commands or local/remote endpoints;
- adapters translate LlamaIndex, Phi, Ollama/LM Studio/llama.cpp-compatible setups, ChatGPT/Claude/etc., or later systems into the neutral contract;
- provider configuration is user-controlled and outside untrusted repository content;
- remote egress must be explicit;
- provider output remains untrusted semantic/retrieval output until mechanically checkable fields are validated.

Do not build an auto-installing marketplace, dependency resolver, or repository-triggered plug-in loader. "Plug-and-play" means a documented stable contract plus easy adapter configuration, not automatic execution of unknown code.

### 9. LlamaIndex and Phi are optional reference integrations

LlamaIndex fits the retrieval provider role; Phi 14B fits an optional semantic-assistance provider role. Neither is required.

Retrieval and local-model assistance must not become a mandatory preprocessing chain. A human or stronger reviewer can work directly through the same semantic contract when those services are absent.

Phi may generate candidate relationships, classifications, adversarial ideas, or summaries, but a downstream reviewer must not be restricted to Phi's candidate set when the review claim requires broader coverage.

### 10. One local command surface over one engine

Prefer one command entry point with subcommands over many independent scripts. Candidate user-facing operations:

- initialize/open review
- show status/next work
- begin a stage/pass
- submit/complete a semantic result
- reopen/revise
- validate
- export/import portable review bundle
- configure/list providers

Names such as `begin-pass` are not frozen. The important structural rule is that all commands call the same workflow/state library rather than reimplementing transition rules.

### 11. GitHub Actions becomes an optional thin wrapper

Normal operation requires **zero GitHub Actions runs**.

If a project wants hosted verification or branch protection, one optional workflow should invoke the same local validation command against the checked-out repository/review bundle. GitHub Actions must not contain a second implementation of review semantics.

This optional wrapper may be run only when a project chooses hosted enforcement; it is not required to advance or complete a review locally.

### 12. Migrate legacy evidence; do not rewrite it

Keep the current merged PR6 system authoritative while the new engine is implemented and reviewed.

Provide a one-way migration/import path that records legacy change records, gates, completions, occurrence history, and results as legacy evidence with their original identities/meaning. The migration may create indexed representations, but must not claim that old evidence satisfied rules invented by the new engine.

Only after the new engine passes its own reviewed transition plan should the canonical operating instructions switch to it.

### 13. Defer dynamic mid-pass subdivision until the core transition engine is stable

The engine/schema must reserve a representable path for subdivision, but dynamic subdivision is not part of the first implementation milestone.

First prove ordinary stage/pass, interruption, reopening, migration, replay protection, provider substitution, breadth accounting, and final completion. Then add subdivision using the same immutable occurrence/lineage model.

This avoids expanding the first refactor while preserving the future option.

## Current-control disposition

The existing control families receive these structural treatments:

- **Adaptive Execution gate/completion evidence:** simplify into workflow-engine transition/plan records; retain semantic/mechanical separation and context-mode evidence.
- **Pass-boundary/handoff chronology:** retain invariant; implement in one state engine/database rather than independent record/hash choreography.
- **Review revision/reopening:** retain as core transition semantics.
- **Occurrence identity/history/replay protection:** retain as immutable database evidence/constraints plus export representation.
- **Artifact/current-state binding:** normalize to snapshot ID and retain.
- **Change-impact records:** retain logical change-impact concept; store as authoritative structured state/events rather than requiring one mutable JSON file per change unless an export consumer needs it.
- **Class-to-stage/evaluation mapping:** retain as canonical configuration because it has a distinct rule-selection function.
- **Generated revalidation queue:** replace as committed artifact; retain only as generated status/plan projection/export.
- **Changed-file coverage:** retain capability locally where a snapshot/diff adapter can establish changed objects; Git adapter supplies current Git-specific implementation.
- **Regression/structural validators:** retain their distinct tests but consolidate shared state logic behind one library/CLI.
- **Git-specific exhaustive inventory controls:** retain as Git adapter/evidence mechanisms for Git exhaustive claims; do not make them universal semantic definitions.
- **GitHub Actions/branch protection:** make optional host enforcement only.
- **Legacy historical evidence:** retain through explicit migration/import compatibility.

## Rejected or deferred structures

- **Three-file `active.json` + `occurrences.jsonl` + `revisions.jsonl`: rejected** as the default because it recreates atomicity/synchronization burden that SQLite solves directly.
- **Pure event-log-only implementation: rejected for the first reference backend** because it requires rebuilding indexing, transaction, locking, and projection machinery already supplied by SQLite.
- **Git commits as the workflow database: rejected** because workflow correctness should not require one commit per state transition and Git history is not a convenient transactional/query API for ordinary users.
- **GitHub as workflow authority: rejected.**
- **Required hosted CI: rejected.**
- **Automatic plug-in installation/discovery from repository content: rejected.**
- **A large generic provider framework before concrete adapters exist: rejected.**
- **Real-time distributed collaboration: deferred.** Portable lineage-aware bundles are sufficient initially.
- **Dynamic mid-pass subdivision in milestone one: deferred.**
- **Optional signed/external checkpoints: deferred** until a user needs stronger tamper evidence than local assumptions provide.
- **Non-Git repository adapters beyond the normalized boundary: deferred** until there is a concrete consumer.

## Why this is lower burden

Compared with the current PR6-era workflow, the selected structure aims to remove or collapse several maintenance surfaces:

- no required GitHub Actions execution;
- no committed revalidation queue churn;
- no LLM-computed hashes or hand-built state transitions;
- no multiple mutable JSON authorities for live workflow state;
- no separate persistence semantics per validator script;
- no hidden post-stage evaluation layer;
- no requirement that optional retrieval/model services exist;
- no plug-in package manager;
- no first-release distributed synchronization system.

The complexity retained is tied to distinct material requirements: transactions/concurrency, snapshot binding, immutable credited evidence, reopening/replay safety, provider trust/egress, breadth accounting, migration, and manual recovery.

## Breadth check

Structural Optimization covered the applicable structural surface rather than optimizing only the newest user requirements: state authority, persistence, collaboration, repository/snapshot abstraction, generated artifacts, evaluation structure, breadth enforcement, providers/adapters, local-model/retrieval integration, command surface, hosted enforcement, migration, dynamic subdivision, existing-control disposition, and deferred features.

Scope-inversion question: **What could still be structurally wrong even if every stated user requirement were satisfied?** A design could still duplicate state authority, choose a merge-hostile or crash-fragile store, preserve hidden evaluations, build an oversized plug-in framework, keep stale generated artifacts, prematurely generalize beyond Git, or preserve PR6 bookkeeping merely because it exists. The selected structure addresses those risks.

No material unnecessary permanent layer or accidental platform/vendor coupling identified in the bounded roadmap remains without a named consumer or explicit deferral.

## Handoff to End-to-end validation

End-to-end validation must trace the selected architecture through at least:

1. fresh local manual review with no models, no LlamaIndex, no GitHub, and zero Actions;
2. local Git review using LlamaIndex retrieval and Phi assistance;
3. optional hosted model with explicit egress permission;
4. normal five-stage completion with visible evaluation/acceptance criteria and breadth evidence;
5. interruption/crash between semantic work and a state transition;
6. stale snapshot/index after source change;
7. blocking finding causing revision/reopening;
8. duplicate/replayed occurrence attempt;
9. concurrent local writer conflict;
10. collaborator/imported bundle with divergent lineage;
11. provider unavailable/schema-invalid/permission-denied fallback to manual or alternate provider;
12. sensitive-data minimization path;
13. legacy PR6 migration/bootstrap path;
14. optional GitHub hosted verification without making local completion depend on it;
15. final completion and later recurrence/reopening;
16. a full-program breadth omission that must be rejected;
17. a future-subdivision placeholder/path showing that deferral does not make the state model incapable of representing later subdivision.

If those traces expose a structural contradiction, reopen the earliest affected stage rather than forcing the architecture through End-to-end validation.

No implementation phase or pull-request breakdown is authoritative until End-to-end validation completes.
