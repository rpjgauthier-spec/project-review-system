# Review-Method Evolution — Living Design Note

## Status and authority

This is a living, non-authoritative design note for the Project Review System local-first refactor.

It records review-method ideas discovered during controller-core recovery and subsequent discussion. It does **not** change the current validated five-stage Project Review System, current stage ordering, or controller-core Slice 1 scope. Any adoption must go through the normal governed change/reopening/cutover path.

This note complements:

- `local-first-refactor-living-design-notes.md`
- `adaptive-model-before-change-design-note.md`

The existing validated Project Review System remains authoritative until a separately governed change is accepted.

## 1. Purpose-preservation / reviewer-induced drift

### Problem

A reviewer can begin with a legitimate correction task, repeatedly improve local defects, and gradually transform the reviewed artifact into something materially different from what the user or governing requirements originally asked for.

This is **review-induced drift**.

It is distinct from ordinary implementation error. The resulting design may be internally coherent and even technically superior along some dimensions while no longer preserving the original purpose, protected scope, non-goals, constraints, or decision rights.

### Design principle

Before substantial solution-space exploration or correction, preserve an explicit model of the **governing intent**.

Potential protected elements include:

- original problem/purpose;
- success criteria;
- required capabilities;
- protected user goals and constraints;
- explicit non-goals;
- scope boundaries;
- authority/decision boundaries;
- required interfaces/compatibility obligations;
- requirements that may be challenged only through explicit escalation rather than silently rewritten.

The implementation is allowed to move. The governing intent is not silently allowed to move with it.

### Important distinction

The system should support both:

1. **de-anchoring from the proposed implementation** — reviewers may discover that the proposed architecture, workflow, decomposition, or mechanism is unnecessarily complex or inferior; and
2. **anchoring to governing intent** — alternative solutions must still satisfy the same protected purpose, requirements, constraints, and decision rights unless those are explicitly reopened and separately authorized.

These are complementary, not contradictory.

A useful rule is:

> Freeze the governing intent and constraints before broad solution-space exploration. Reviewers may challenge or replace implementation structure, but may not silently alter protected objectives, scope, requirements, non-goals, or user-controlled decisions.

### Purpose-preservation delta

After a material correction or redesign, the review should be capable of asking:

- Which governing requirements changed?
- Which protected invariants changed?
- Which non-goals became goals, or goals became non-goals?
- Did scope expand or contract?
- Did any authority or decision right move?
- Did an implementation convenience become a requirement?
- Did a reviewer solve a different problem than the one originally governed?

An unintended material change in protected intent should block ordinary correction credit and require explicit redesign/requirements authorization.

### Relationship to adaptive model-before-change reasoning

The adaptive model-before-change capability is a natural place to preserve this baseline.

For a substantial change, the minimum useful model should include the protected intent/constraints when those could be affected. The change-impact/delta step should compare both implementation behavior **and purpose preservation**.

Do not require a separate permanent intent document for trivial changes when the authoritative requirements already provide a clear baseline.

## 2. Structural Optimization should be aggressively reductive

### Existing direction

The current Structural Optimization module already asks whether elements have distinct consumers/functions, whether simpler mechanisms are equivalent, whether permanent artifacts are justified, whether review depth is proportionate, and whether implementation assumptions are being mistaken for requirements.

The redesign should preserve and sharpen that role.

### Stronger redesign requirement

Structural Optimization should actively attempt to eliminate unnecessary complexity rather than merely tidy the proposed structure.

Candidate rule:

> Every material component, phase, artifact, command, authority boundary, review obligation, persistent state, interface, adapter, generated projection, and recurring duty must justify its continued existence through at least one distinct requirement, invariant, lifecycle, consumer, security/access boundary, failure/recovery mode, or material reduction in risk. If it cannot, prefer removal, merger, deferral, narrowing, generation, or simplification.

The following are not sufficient justification by themselves:

- it already exists;
- it was in the proposal;
- it is organized cleanly;
- it might be useful later;
- another artifact currently refers to it when that dependency exists only because both were introduced together;
- removing it would require changing adjacent prose or code.

### Complexity proportionality test

Add an explicit proportionality question:

> Is the machinery introduced to control, review, represent, or mitigate the problem becoming comparable to or more complex than the problem/system it governs, without proportional reliability, safety, recoverability, or risk reduction?

If yes, Structural Optimization should treat the complexity itself as a finding requiring explicit justification or reduction.

This is especially important for governance/review systems, where controls can recursively generate more controls, documents, evaluators, handoffs, and state.

### Recursive-complexity check

When a proposed control exists mainly to manage complexity introduced by an earlier control, reviewers should trace the chain backward and ask whether the original control can be simplified or eliminated instead.

Conceptually:

```text
control A creates burden
    -> control B manages A's burden
    -> control C verifies B
```

Before accepting C, test whether A can be redesigned so B and C disappear.

### Anti-bureaucracy objective

The objective is not minimum file count or minimum lines. The objective is **minimum justified system burden** while preserving required capability and safeguards.

A larger structure may be correct when distinct authority, lifecycle, consumers, security boundaries, or failure modes require it. The reviewer must make that justification explicit rather than assuming separation is prudent.

## 3. Candidate evolution of the review-stage model

The current validated semantic stages are:

1. Adversarial
2. Interdependency
3. Normalization
4. Structural Optimization
5. End-to-end validation

Do not change this sequence merely because additional useful review dimensions have been identified.

The following are candidate future review concerns that may warrant either new core stages or adaptive review dimensions.

### Intent Preservation

Core question:

> Does the reviewed/corrected artifact still solve the governed problem without silently changing protected purpose, scope, constraints, non-goals, requirements, or decision rights?

Potential placement: early, before reviewers are allowed to substantially reshape the solution.

Reason it may deserve distinct ownership: no current stage clearly owns systematic protection against reviewer-induced purpose drift.

### Failure & Recovery

Core question:

> What happens under interruption, stale state, partial success, corruption, dependency failure, retry, rollback, unavailable authority, or other abnormal execution paths, and can the system recover without fabricating state or losing required evidence/authority?

Potential placement: late, after the structure stabilizes and before final end-to-end validation.

Reason it may deserve distinct ownership: End-to-end validation includes failure paths, but a dedicated stage could perform deeper abnormal-path and recoverability analysis rather than treating failure as one subset of representative integrated traces.

### Assumption / Evidence quality

Questions:

- Which decisions rely on assumptions?
- Which assumptions are verified versus inferred?
- Are external facts, estimates, environmental conditions, or requirements being treated as settled without sufficient evidence?
- Which assumptions must be validated before downstream conclusions are reliable?

This may fit better as an adaptive review dimension than a mandatory stage.

### Requirements coverage

Questions:

- Is every governing requirement represented in the design/implementation?
- Is every major mechanism justified by a governing requirement/invariant?
- Are there orphan requirements or orphan mechanisms?

Parts may be deterministic when requirements are structured. This may fit as an adaptive evaluation rather than a mandatory semantic stage.

### Operability / maintainability

Questions:

- Can a future human or AI understand, operate, debug, recover, and safely modify the result?
- Are diagnostics and ownership clear?
- Is remaining complexity manageable?
- Will routine maintenance require reconstructing hidden context?

This may be an adaptive dimension, potentially consumed by Structural Optimization and End-to-end validation.

## 4. Core stages versus adaptive review dimensions

Rather than continually expanding a fixed stage list, consider a two-layer design:

```text
ordered core semantic stages
        +
adaptive review dimensions/evaluations
```

Possible adaptive dimensions include:

- intent preservation;
- failure/recovery;
- security;
- safety;
- maintainability/operability;
- performance;
- evidence quality;
- requirements coverage;
- privacy;
- migration/backward compatibility;
- domain-specific hazards.

The controller/reviewer should select only dimensions materially relevant to the target/change.

A dimension may eventually graduate to a core stage if experience shows that:

- it is broadly applicable;
- omission repeatedly causes material defects;
- no existing stage can own it cleanly without dilution;
- ordered placement is important to later reasoning;
- making it adaptive produces inconsistent coverage.

Conversely, do not add a core stage merely because a useful question exists.

## 5. Relationship to model-before-change reasoning

Adaptive model-before-change reasoning can support these review dimensions without becoming a reviewer of its own.

Examples:

- governing-intent model -> purpose-preservation checks;
- state/transition model -> failure/recovery analysis;
- dependency/authority map -> Interdependency;
- component/consumer model -> Structural Optimization;
- requirements mapping -> coverage evaluation;
- interface/operational model -> maintainability/operability analysis.

The key principle remains:

> Select the minimum sufficient reasoning representation for the actual risk.

Do not generate all models for every target.

## 6. Guardrail against the reviewer morphing the system

A future Project Review System should distinguish at least three outcomes for a proposed change:

1. **correction** — preserves governing intent while repairing a defect;
2. **structural alternative** — materially changes implementation/design structure while preserving governing intent;
3. **requirements/redesign change** — materially changes protected purpose, scope, requirements, non-goals, authority, or user decision rights.

The first two may proceed through ordinary review when authorized. The third must be explicitly surfaced and separately authorized; it must not be disguised as a correction.

This classification should fail closed when the distinction is uncertain.

## 7. Open design questions

- Should Intent Preservation become a sixth core stage, an early pre-review gate, or an adaptive dimension?
- Should Failure & Recovery become a seventh core stage or remain a strong required dimension of End-to-end validation for high-risk/stateful targets?
- How should governing intent be represented without freezing accidental implementation detail?
- Which requirements are protected from reviewer modification versus legitimately challengeable?
- How should explicit user authorization to change the problem definition be represented?
- How should purpose-preservation delta checks interact with change-impact/revalidation mapping?
- Can requirements coverage be partially deterministic without overclaiming semantic completeness?
- How should complexity proportionality be assessed without turning a subjective heuristic into deterministic authority?
- What evidence should justify retaining a control whose complexity exceeds the underlying mechanism it governs?
- How should recursive governance/control complexity be detected and surfaced?
- Which adaptive dimensions should be selected automatically versus explicitly requested?
- What empirical dogfooding evidence should be required before promoting a review dimension into the permanent core stage sequence?

## 8. Current implementation boundary

Do not modify current production stage definitions, current Structural Optimization authority, or controller-core Slice 1 solely because this note exists.

The immediate purpose is to preserve the discovered design ideas so they can be deliberately incorporated into the reviewed local-first redesign rather than being lost, silently mixed into recovery instructions, or prematurely treated as validated governance.
