# Structural Optimization Review

## Mission

Select the lowest-burden reliable structure that preserves capability, safety, authority, evidence, recoverability, restrictions, access boundaries, traceability, independent lifecycles, and useful future options.

This stage includes minimalism, but it is not limited to removal. It may retain, defer, narrow, simplify, merge, split, index, generate, restructure, generalize, specialize, or remove elements when the resulting design is materially better and no required protection or consumer is lost.

Run this after adversarial, interdependency, and normalization review for a full program. For a focused review, use it alone only when prior safety, authority, and dependency conclusions remain valid for the bounded change.

Bounded revalidation is not a sixth review stage. It is a change-triggered lifecycle mechanism that selects and reruns affected conclusions from the five-stage model. Structural Optimization may assess whether the selected revalidation scope and supporting artifacts are proportionate, but it does not own or redefine the canonical revalidation mapping, reopening order, or advancement gate.

## Optimization questions

Apply only relevant questions:

1. What distinct function and consumer does the element serve?
2. What failure, loss, misuse, or recovery need does it prevent?
3. Is its trigger active, conditional, historical, or absent?
4. Does another element already perform the function?
5. Can a simpler mechanism preserve equivalent reliability?
6. Would removal lose a safeguard, authority, restriction, evidence, or recovery path?
7. Is deferral, narrowing, merging, splitting, indexing, generation, generalization, or specialization safer than removal?
8. Does one fact force unnecessary updates across multiple records?
9. Is the selected review depth proportionate to the question?
10. Does a permanent tracker, report, role, status, or recurring review have a distinct ongoing consumer?
11. Do related artifacts share authority, schema, lifecycle, update trigger, access permissions, retention rules, and consumers closely enough to consolidate?
12. Is an artifact overloaded with unrelated authorities, lifecycles, permissions, or consumers and therefore safer to split?
13. Would structured data plus generated views reduce duplicated maintenance without obscuring authority?
14. Does the proposed organization reduce update cascades, navigation burden, and inconsistent copies?
15. Is a function coupled to a particular platform, storage medium, implementation, domain, artifact type, or vendor even though the function itself does not require that coupling?
16. Can invariant behavior be separated from environment-specific evidence, enforcement, transport, or storage mechanisms without adding unjustified abstraction or weakening controls?
17. Is a stated scope constraint functionally necessary, or has an implementation assumption been mistaken for a requirement?

## Abstraction-boundary analysis

When a capability may be reusable beyond its current environment, distinguish:

- **invariant semantics** — behavior required regardless of platform or storage medium;
- **environment-specific evidence** — identifiers, manifests, paths, metadata, or coverage mechanisms needed only in a particular environment;
- **environment-specific enforcement** — CI, hooks, permissions, branch rules, APIs, or other host controls;
- **domain-specific policy** — constraints that are genuinely part of the reviewed domain rather than reusable method.

Do not generalize merely because reuse is imaginable. Generalization is justified only when the core function does not depend on the current environment and separating the boundary reduces false assumptions, duplication, or future rework without materially increasing complexity.

Likewise, do not force generic abstractions over mechanisms whose correctness actually depends on a specific host, data model, or evidence source.

## Artifact-family analysis

For each material family of related artifacts, compare the current arrangement with these alternatives:

- keep separate
- merge into one canonical artifact
- use one artifact per category
- use a template plus instances
- use structured data plus generated consumer views
- create an index or manifest over independent records
- split an overloaded artifact
- separate generic semantics from environment-specific adapters
- archive dormant instances
- defer redesign until a named trigger occurs

Fewer files are not automatically better. Consolidation normally requires compatible authority, schema, lifecycle, update trigger, access permissions, retention rules, and consumers. Preserve separation where it reduces concurrency conflicts, confidentiality risk, independent-lifecycle coupling, unstable references, or ownership ambiguity.

## Finding classes

- duplicate control
- unused output
- premature feature
- excessive gate
- update cascade
- speculative detail
- historical-as-active
- over-specified workflow
- unnecessary authority
- unnecessary permanent artifact
- excessive review depth
- fragmented artifact family
- overloaded artifact
- duplicated schema or prose
- unsuitable representation
- unnecessary synchronization
- simpler equivalent
- accidental environment coupling
- implementation assumption treated as requirement
- premature generalization
- missing abstraction boundary

Length, inconvenience, low frequency, file count, or preventive purpose alone do not prove poor structure.

## Correction preference

Choose the least disruptive reliable treatment. Common dispositions include:

1. retain
2. defer
3. narrow
4. simplify
5. index or generate
6. generalize or specialize at a justified boundary
7. merge or split
8. remove

Use the canonical dispositions in `shared-control-model.md`. Record a clear justification when the best structural treatment does not map exactly to a disposition label.

## Anti-expansion rule

Do not create a permanent document, tracker, checklist, status, role, recurring review, evaluation obligation, generated view, adapter layer, or update duty unless an existing mechanism cannot reliably serve the material consumer.

Do not require the full review program for a focused question when one or two modules plus direct-dependency inspection can answer it safely.

## Validation

For each material change:

- verify normal behavior
- test a relevant failure or missing-input case
- verify direct dependencies, authorities, and consumer paths
- confirm no silent authorization was introduced
- confirm restrictions and historical evidence remain usable
- confirm reversibility or justify safe irreversible loss
- confirm removed or consolidated artifacts had no distinct remaining consumer
- confirm split artifacts preserve a discoverable controlling authority
- confirm access, retention, and lifecycle boundaries remain correct
- confirm generated views cannot override their source authority
- confirm generic semantics do not silently absorb environment-specific guarantees
- confirm environment-specific mechanisms remain specific when their correctness depends on that environment
- confirm the selected review depth still covers the bounded risk
- perform the backward-impact gate required by `shared-control-model.md`

A stage is `Complete` when no material unnecessary burden, accidental coupling, unjustified abstraction, or materially inferior structure remains within the reviewed scope under the current state and known triggers. It may be `Conditional` when named external facts determine whether a dormant structure activates, remains deferred, or should be reorganized.