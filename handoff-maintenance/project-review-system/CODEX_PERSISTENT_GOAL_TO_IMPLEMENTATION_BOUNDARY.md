# Codex Persistent Goal — Through Implementation Boundary

Use this as the persistent `/goal` instruction for the current Project Review System work.

## Goal

Continue from the current durable repository state until:

1. the bounded controller-core recovery is validly complete;
2. the local-first PRS design has completed its required governed review and convergence; and
3. an implementation-ready specification is durably recorded.

**Stop there. Do not implement the new local-first deterministic PRS engine.**

## Operating rules

At the start of each continuation, re-establish current repository and PRS authority from durable evidence and derive the next permitted activity from that state.

For any semantic activity:

- verify it is the next permitted activity and that the current execution satisfies the required semantic boundary;
- establish, validate, and durably record whatever current PRS requires before semantic work begins;
- perform only that bounded semantic activity;
- validate and durably record its completion before later work receives current credit.

Do not perform multiple PRS-separated semantic activities inside one execution. A `/goal` continuation is not, by itself, proof of a valid semantic boundary. If the required boundary cannot be established from trustworthy available evidence, stop rather than simulate or self-attest it.

Preserve historical durable evidence and chronology. If a correction invalidates existing credit, follow current PRS reopening and revalidation rules. Do not alter historical evidence to manufacture current credit.

Continue deterministic bookkeeping, validation, state/queue maintenance, commits, and other non-semantic work automatically when current PRS permits it. Treat evaluations according to the execution/boundary requirements PRS assigns to them.

When progress conflicts with uncertainty about authority, review credit, or boundary validity, fail closed and preserve correctness rather than forcing advancement.

## Completion checklist

This checklist is descriptive, not authority. If current repository or PRS authority changes, supersedes, or makes an item inapplicable, follow current authority and disposition the item rather than forcing it.

- [ ] Finish the current controller-core recovery, including all required remaining review/evaluation/closure work.
- [ ] Establish the current authoritative local-first refactor design state.
- [ ] Complete its remaining governed review, including any required corrections, reopenings, or backward-impact work.
- [ ] Reach design convergence.
- [ ] Durably record an implementation-ready specification sufficient for a separate implementer to build and test the system without making new architectural decisions.
- [ ] Stop before implementation.

## Implementation-ready boundary

The specification should capture the reviewed contracts needed for implementation, including applicable authority, lifecycle/state transitions, semantic interfaces, persistence/state requirements, recovery/idempotency/concurrency behavior, validation and completion rules, trust/provider boundaries, migration requirements, portability constraints, and acceptance criteria.

Keep this at the contract/invariant level. Do not produce production code, executable pseudocode, implementation bodies, migration scripts, or file-by-file coding instructions except for non-executable interface/schema artifacts explicitly required by the reviewed design.

## Hard stop

Do **not**:

- implement the new local-first engine;
- create production controller/state/persistence code;
- implement the selected database/backend;
- implement production commands such as `begin-pass`, `complete-pass`, `status`, or `repair`;
- create migration/cutover code;
- create a prototype or skeleton to test the design;
- begin implementation-driven debugging or rewrite cycles.

Implementation will be performed separately and returned later for governed validation and real-world dogfooding.

If the normal workflow would proceed from design completion into implementation, treat the durably recorded implementation-ready specification as the terminal state for this goal and stop.

Before that terminal state, stop only for a genuine blocker requiring user judgment/authorization, unavailable credentials/access, unresolvable authority, or a required semantic boundary the current host execution cannot validly establish.

Do not expand beyond this governed recovery/design scope.