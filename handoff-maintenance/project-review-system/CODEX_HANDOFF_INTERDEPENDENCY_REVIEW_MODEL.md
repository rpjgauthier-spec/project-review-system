# Codex Handoff Interdependency Review Model

## Invocation contract

Use this stage model through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before a full Interdependency review, complete Model Before Review for the current handoff revision. Derive the concrete dependency graph from the current Lean target rather than copying its prose sequence into this model.

Refresh this model only when the stage's stable dependency categories or material failure families change.

This is a handoff-maintenance aid, not Project Review System authority.

## Purpose

Find broken, missing, duplicated, circular, stale, or ownerless relationships in the recovery handoff by testing how authorities, evidence, states, actions, and outputs depend on one another.

A discovered dependency defect is a candidate problem, not automatically a handoff feature request. After the sweep, run the mandatory Ownership Test before proposing any correction.

## Pass completion

A full Interdependency pass is complete only when:

- every handoff section has been mapped into the current dependency graph;
- every material producer/consumer relationship has been tested;
- every authority-to-action and evidence-to-conclusion edge has been tested;
- every material handoff, propagation duty, fallback, and completion dependency has been tested;
- each material producer/consumer edge has been closed across the target-derived producer states that can change consumer reachability or downstream obligations;
- circular, duplicated, missing, stale, and ownerless dependencies have been challenged;
- the bounded dependency inventory is explicitly closed under the shared coverage rule from `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`;
- the complete blocker/high candidate set has been collected before reporting.

Do not stop at the first broken edge.

## Interdependency coverage closure

Use the existing node/edge model as the coverage witness. For each material producer/consumer edge, derive only producer-state variants that can change behavior for the current target, such as present/current, missing, stale, conflicting, or changed.

For each applicable variant, verify whether the consumer is reachable, whether its prerequisites remain valid, what downstream obligation is triggered, and whether failure reaches the correct fallback or blocker.

Do not create a universal state matrix. Close only the target-derived producer states and consumer paths with material consequences.

## Governing purpose

The handoff exists to help Codex locate current authority, recover the specific controller-core review failure through production PRS, and stop at the next valid governed state or real blocker.

Interdependency review asks whether the pieces needed for that recovery are connected correctly without turning the handoff into a second PRS.

## Derive the current dependency graph

During Model Before Review, derive the current Lean graph using nodes only where they have a material consumer.

At minimum consider these node classes when present:

- repository / remote / locator;
- applicable repository authority;
- production PRS controls;
- review-state authority;
- source-scope authority;
- host/user task authorization;
- historical recovery pointers and evidence;
- deterministic failure/checker evidence;
- governed next action;
- correction/validation path;
- stop condition / blocked recovery;
- final recovery report.

For each node identify:

1. **producer** — what source establishes it;
2. **consumer** — what later decision/action depends on it;
3. **binding** — which repository/ref/revision/target/occurrence it belongs to when material;
4. **propagation duty** — what must change or be re-established if the producer changes;
5. **fallback/blocker** — what happens if the dependency cannot be satisfied;
6. **owner** — handoff, production PRS, repository/governance, or host/user context.

Do not add a node merely because one can be imagined. Model only relationships material to the current recovery.

## Stable relationship classes to test

### Authority → governed interpretation/action

Any instruction depending on authority must identify or defer to the source that owns that authority. The handoff must not manufacture the missing edge.

### Host/user authorization → external/repository action

Actual action permission must derive from host/user task authority and must remain distinct from PRS-governed mode, scope, and transitions.

### Evidence → conclusion

A conclusion may consume evidence only within the identity and temporal scope that evidence actually supports. Historical evidence cannot silently become current authority or review credit.

### Producer → consumer

Every required consumer must have a reachable producer. Every permanent producer/reference in the handoff should have a material consumer.

### State change → downstream invalidation/refresh

When a material producer changes, test whether downstream assumptions, evidence, or conclusions must be re-established. Do not reproduce PRS revalidation mechanics in the handoff; verify that Lean delegates them to PRS where PRS owns them.

### Handoff → PRS

Lean should provide recovery-specific navigation and then hand PRS-owned behavior to production PRS. Test for missing handoff edges and for shadow-PRS duplication.

### Failure → fallback/blocker

Every material dependency failure should either reach an owner-provided recovery path or a truthful blocker. The handoff must not improvise a replacement authority or transition.

### Completion → report/stop

Successful recovery, blocked recovery, and fresh semantic-boundary stops must propagate to the final report without being confused with one another or with ordinary feature continuation.

## Interdependency dimensions

Sweep the target across these dimensions:

A. **Producer completeness** — does every material consumed fact/action have a producer?

B. **Consumer justification** — does every retained handoff element have a material consumer?

C. **Authority edge** — does each governed decision consume authority from the correct owner?

D. **Identity binding** — can a consumer accidentally use evidence from the wrong repo/ref/record/revision/target/occurrence?

E. **Temporal dependency** — can stale evidence or an earlier state survive after its producer changes?

F. **Propagation** — when a producer changes, are affected consumers re-evaluated by the owning system?

G. **Handoff contract** — is responsibility transferred cleanly to production PRS rather than duplicated or dropped?

H. **Fallback** — does a broken dependency fail closed or invent a substitute?

I. **Circularity** — does A require B while B requires A, especially around authority, state, or authorization?

J. **Duplication** — are two nodes/rules pretending to own the same relationship, creating drift risk?

K. **Orphaning** — is there a rule, pointer, section, report field, or mechanism with no material downstream consumer?

L. **Completion propagation** — do success, blocked recovery, and execution-boundary stops reach the correct final state/report?

## Minimum failure families

Challenge at least:

1. locator points to implementation but no valid edge establishes review-state continuity;
2. PRS controls are referenced but applicability cannot be established by repository authority;
3. review-state facts are consumed before their owning source is established;
4. source-scope authority changes but bounded recovery assumptions are not reconsidered;
5. host/user authorization is conflated with PRS governance;
6. historical evidence is consumed as current authority or current credit without a valid edge;
7. a current checker result is used to rewrite historical authority;
8. recovery pointers become authoritative rather than navigational;
9. a PRS-owned dependency is duplicated in Lean and can drift;
10. a Lean-specific rule has no recovery-specific consumer;
11. a required dependency has no producer and no explicit blocker;
12. fallback creates new authority, succession, or transition machinery;
13. correction changes upstream state but downstream recovery evidence remains stale;
14. blocked recovery is reported as successful completion;
15. successful recovery flows into ordinary feature implementation;
16. final report omits the material state needed by the next consumer.

Do not create permanent handoff machinery solely to handle a hypothetical dependency with no material current consumer.

## Finding standards

### Blocker

Use when a broken dependency can cause unauthorized action, invented governance, false review credit, operation on the wrong identity/state, invalid recovery transition, falsified history, or inability to determine a truthful next action.

### High

Use when a broken dependency materially raises the probability of stale evidence use, dropped propagation, ambiguous ownership, incomplete validation, misleading completion, or recovery dead-end.

Do not elevate cosmetic ordering or documentation preferences unless they break a material relationship.

## Ownership test after the sweep

Classify every blocker/high candidate using `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`:

- **handoff-owned** — Lean itself breaks or omits a recovery-specific dependency;
- **production-PRS-owned** — PRS owns the relationship; reference/defer rather than duplicate;
- **repository/governance-owned** — required authority/relationship is absent or unresolved; report rather than invent;
- **no material owner/value** — redundant, theoretical, or mitigation costs as much as the risk reduced.

Only handoff-owned candidates may proceed to Model Before Change and Structural Optimization.

## Structural pressure after ownership

For each handoff-owned candidate ask:

- Is the dependency recovery-specific?
- Can an existing authoritative edge already carry it?
- Can one general relationship replace multiple local rules?
- Does the proposed fix create a second producer/owner for the same behavior?
- Would deleting an orphan be safer than wiring it into more machinery?

Prefer deletion, delegation, or one clear edge over new permanent structure.

## Review cycle and convergence

```text
Model Before Review
    -> derive current dependency graph and bounded producer-state inventory
    -> close producer-state × consumer-reachability obligations
    -> full Interdependency sweep
    -> complete blocker/high candidate set
    -> Ownership Test
    -> Model Before Change for handoff-owned candidates
    -> survive-or-die
    -> apply only survivors
    -> repeat only while surviving handoff-owned blocker/high corrections remain
```

Convergence is governed by `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
