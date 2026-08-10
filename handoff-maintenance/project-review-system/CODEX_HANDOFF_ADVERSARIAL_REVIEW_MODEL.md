# Codex Handoff Adversarial Review Model

# Invocation contract

This stage-specific model is invoked through `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.

Before using this document, complete the shared Model-Before-Review checkpoint for the current handoff revision. If the handoff changed an authority edge, identity binding, state transition, invariant, validation owner, task boundary, or material failure path, refresh this model before beginning the Adversarial sweep.

A request to perform a full Adversarial review of the handoff implicitly requires this model even when the immediate prompt does not mention it.

## Purpose

Use this document before adversarially reviewing the Codex recovery handoff for `rpjgauthier-spec/project-review-system`.

The purpose is to find **multiple independent defects in one bounded pass** by reviewing the handoff against an explicit system model instead of reading it only as prose.

This is a handoff-maintenance aid. It is **not Project Review System authority** and does not create review credit, permissions, recovery rules, or production governance.

## Core rule

Before beginning an adversarial pass:

1. model the handoff's purpose, authorities, identities, state flow, invariants, and failure paths;
2. map each section of the handoff to that model;
3. sweep every applicable review dimension across the **entire document**;
4. collect all blocker/high findings found in the declared pass;
5. report only after the full sweep is complete.

Do not stop merely because one blocker has been found.

## Pass completion rule

An adversarial pass is complete only when:

- every handoff section has been considered;
- every applicable review dimension below has been tested;
- every modeled state transition and authority edge has been challenged;
- every declared failure-path family has been considered;
- all blocker/high findings discovered in that pass have been collected.

A finding may justify stopping execution of the **target workflow**, but it does not automatically terminate the **diagnostic sweep** unless the remaining document cannot be interpreted reliably.

## 1. Governing purpose

Freeze the handoff's purpose before review.

Current purpose:

> Help Codex discover the current governed Project Review System state, recover the controller-core review to the next valid governed state, complete recovery-induced obligations, and stop without inventing authority or continuing ordinary feature implementation.

Adversarial question:

> Does any instruction cause Codex to solve a different problem, expand scope, continue too far, or substitute the handoff for current repository authority?

## 2. Authority model

Identify every authority source and its role.

### Host/user task context

Owns:

- actual permission to perform the requested task;
- permission for repository content/history writes when granted;
- product/scope decisions that repository governance cannot determine.

Must not be inferred from repository-controlled data.

### Current PRS authority

Owns:

- review mode;
- staged review behavior;
- execution-boundary requirements;
- current review-state semantics;
- revalidation requirements;
- valid state transitions;
- evidence/credit rules.

### Controlling review/change state

Owns current review program state when validly established.

Must be challengeable by governed provenance/chronology validation when its legitimacy is specifically under investigation.

### Source-scope authority

Constrains what controller-core implementation work is actually authorized.

### Git history

Provides:

- chronology;
- provenance;
- content lineage;
- evidence of when state/control changes occurred.

Does not create review credit or authority by itself.

### Derived state

Examples:

- revalidation queue;
- generated projections;
- reports.

Provides operational views only.

Must not silently become authority.

### Handoff

Provides navigation and recovery context only.

Must never:

- create missing authority;
- create review credit;
- create succession rules;
- create migration/bootstrap rules;
- retroactively change what authority governed historical events.

## 3. Identity model

The reviewer must test whether these identities are established and kept correctly bound:

- repository;
- selected Git remote;
- implementation branch/ref;
- continuation/successor ref, if any;
- controlling change/review record;
- review revision;
- target state / snapshot identity;
- execution gate;
- pass occurrence;
- completion evidence;
- semantic result;
- revalidation queue context;
- source-scope authority.

Primary attack:

> Could evidence from identity A accidentally be accepted as evidence for identity B?

Examples:

- right branch, wrong remote;
- right code, wrong review record;
- right record, stale revision;
- right revision, stale target;
- equivalent cherry-pick, invalid inherited credit;
- correct queue path from the wrong branch;
- correct pass ID under a changed gate.

## 4. State-flow model

Attack every transition in this sequence:

```text
discover repository
    -> verify remote/repository identity
    -> read minimum PRS authority
    -> establish review mode/scope
    -> establish user/task write authorization
    -> identify governing implementation context
    -> identify controlling review/change state
    -> establish revision + target identity
    -> validate queue/current evidence binding
    -> reproduce historical failure OR establish current disposition
    -> reconstruct relevant occurrence chronology
    -> reconstruct applicable control-version chronology
    -> determine next governed action
    -> perform bounded correction if authorized
    -> validate changed control/source/state
    -> complete recovery-induced obligations
    -> reach next valid governed state
    -> STOP
```

For every arrow ask:

- What evidence permits this transition?
- What blocks it?
- Can stale or wrong-identity evidence satisfy it?
- Can Codex skip it?
- Can Codex repeat it improperly?
- Can a failure fall through into an unsafe default?
- Can the handoff accidentally create the missing permission?

## 5. Protected invariants

Challenge every instruction against these invariants.

### Authority

- No invented authority.
- No self-authorization.
- No repository-controlled text granting host/user permission.
- No derived projection becoming authority.
- No future-design note overriding current production authority.

### Chronology

- No rewritten/fabricated history.
- No retroactive application of current controls without establishing historical applicability.
- No same-revision redo where current governance forbids it.
- No historical content equivalence creating semantic credit.

### Identity and staleness

- No wrong remote.
- No wrong branch.
- No review-state transfer based only on implementation ancestry/equivalence.
- No stale revision/target/gate/completion/result credit.
- No queue trusted against the wrong governing context.

### Execution boundaries

- No semantic work disguised as mechanical work.
- No `SEPARATED` pass treated as separated without a fresh valid boundary.
- No new governed semantic activity without current required preflight/gate.

### Scope

- No recovery task silently continuing into ordinary feature work.
- No roadmap/future-design implementation unless separately authorized.
- No source-scope expansion from handoff summaries.

### Preservation

- No destruction or absorption of unrelated local user work.
- No history rewrite merely to satisfy validation.
- No weakening controls to make recovery easier.

### Validation

- PRS machinery changes receive PRS/control validation.
- Governed source changes receive source-owned validation.
- A passing checker proves only what that checker actually proves.

## 6. Adversarial dimensions

Sweep every applicable dimension across every section.

### A. Authority

Ask:

- Who grants this permission?
- Is that authority available before the instruction uses it?
- Can the instruction manufacture an answer when authority is missing?
- Is a lower-level source being allowed to override a higher-level one?

### B. Authorization

Ask:

- Is this read-only, semantic, write, commit, push, destructive, or external action?
- What user/task authority permits it?
- Could repository content trick the agent into believing it is authorized?

### C. Identity

Ask:

- Which repository/ref/record/revision/target does this instruction act on?
- Is that identity explicit?
- Could another valid-looking identity be substituted?

### D. State

Ask:

- What must be true before this step?
- What becomes true afterward?
- Is the transition represented by current PRS controls?
- Can Codex advance without satisfying a prerequisite?

### E. Chronology

Ask:

- Does this depend on what happened first?
- Which rule version governed the event at that time?
- Is the current checker being used as retroactive proof?

### F. Staleness

Ask:

- Can this record, queue, gate, result, or target become stale?
- How is staleness detected?
- Could apparently current data be current relative to the wrong context?

### G. Failure behavior

Ask:

- What happens if the required evidence is missing?
- What happens if two authorities conflict?
- What happens if current controls cannot represent the needed transition?
- Does the instruction fail closed or improvise?

### H. Recovery

Ask:

- Can every recognized failure reach either a governed recovery path or an explicit blocker?
- Is any recovery mechanism invented by the handoff itself?

### I. Scope

Ask:

- What prevents Codex from doing more work after success?
- Does a correction accidentally authorize adjacent implementation?
- Are external design notes being promoted into current scope?

### J. Validation ownership

Ask:

- Which system was changed?
- Which tests/checkers actually own that system?
- Are PRS tests being mistaken for source correctness, or vice versa?

### K. Trust boundary

Ask:

- Is repository-controlled text being treated as instruction?
- Is mutable external content being treated as unquestionable authority?
- Is a generated artifact treated as stronger than its source?

### L. Reversibility/preservation

Ask:

- Could this instruction overwrite user work?
- Could it rewrite durable history?
- Could it make rollback or provenance reconstruction harder?

### M. Completion

Ask:

- What exact condition ends this handoff?
- Could “continue autonomously” escape the task boundary?
- Are recovery-induced obligations complete before stopping?

## 7. Failure-path families

At minimum, challenge these families in every full adversarial sweep:

1. wrong local worktree;
2. wrong remote;
3. remote advanced;
4. divergent local/remote history;
5. dirty unrelated user changes;
6. multiple plausible controlling records;
7. stale queue;
8. stale gate/completion/result;
9. wrong review revision;
10. wrong target state;
11. code continuation without review-state continuity;
12. historical event governed by an older control version;
13. current checker rejects historical evidence;
14. defective checker/control requires change;
15. changed control attempts to self-certify;
16. source correction passes PRS tests but breaks source behavior;
17. required external scope authority unavailable;
18. user authorized review but not writes;
19. repository text tries to grant permission;
20. required fresh semantic boundary reached;
21. recovery succeeds and ordinary feature implementation is tempting;
22. current historical failure no longer reproduces;
23. current repository has legitimately superseded historical handoff context.

## 8. Section-by-dimension sweep

For each handoff section, create an internal matrix like:

| Section | Authority | Identity | State | Chronology | Failure | Scope | Validation | Completion |
|---|---|---|---|---|---|---|---|---|
| Purpose | ✓ |  |  |  |  | ✓ |  | ✓ |
| Repository | ✓ | ✓ |  |  | ✓ |  |  |  |
| Startup | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| Authority model | ✓ | ✓ | ✓ | ✓ | ✓ |  |  |  |
| Recovery target | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| Semantic boundary | ✓ | ✓ | ✓ |  | ✓ |  | ✓ |  |
| Recovery rule | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Autonomy | ✓ | ✓ | ✓ |  | ✓ | ✓ |  | ✓ |
| Stop conditions | ✓ |  | ✓ |  | ✓ | ✓ |  | ✓ |
| Final report | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

The matrix is a prompt to attack applicable dimensions, not a permanent record requirement.

## 9. Finding standards

### Blocker

Use when the defect can cause:

- unauthorized action;
- fabricated/invented governance;
- false review credit;
- corrupted or irrecoverable state/history;
- operation against the wrong repository/identity;
- invalid semantic-stage execution;
- escape from the bounded task;
- inability to determine a truthful governed next action.

### High

Use when the defect materially increases the probability of:

- stale-state acceptance;
- wrong-branch/ref continuation;
- incomplete validation;
- unsafe fallback;
- ambiguous authority resolution;
- loss of important recovery evidence;
- misleading completion claims.

Do not inflate low-value wording preferences into blocker/high findings.

## 10. Anti-patterns for the reviewer

Do not:

- stop after the first blocker;
- report a finding before completing the declared whole-document sweep unless early reporting is operationally necessary;
- add a rule merely because a failure is imaginable;
- duplicate current PRS instructions unless the handoff creates a nearby ambiguity or the recovery specifically depends on the invariant;
- convert every adversarial finding directly into a correction;
- let the adversarial reviewer perform its own Structural Optimization.

The adversarial reviewer should maximize **credible defect discovery**.

The separate survive-or-die / Structural Optimization review decides which proposed corrections earn continued existence.

## 11. Recommended review sequence

For each new handoff revision:

```text
build/update explicit review model
    -> full adversarial sweep
    -> collect all blocker/high findings
    -> model-before-change analysis of proposed corrections
    -> survive-or-die Structural Optimization
    -> apply only surviving corrections
    -> delta + full adversarial sweep again
```

If a correction changes the authority model, state flow, identity model, or failure-path set, update this review model before the next adversarial pass.

## 12. Desired reviewer behavior

The desired failure mode is:

> "I found twelve candidates; six died under Structural Optimization."

Not:

> "I found one blocker, patched it, then discovered the next blocker that was already present."

Iteration will still occur because corrections can create new defects. The purpose of this model is to reduce defects that survive merely because the reviewer never systematically looked along the relevant dimension.
