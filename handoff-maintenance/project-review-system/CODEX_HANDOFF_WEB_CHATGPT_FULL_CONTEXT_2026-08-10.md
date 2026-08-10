# Web ChatGPT Handoff — Project Review System

## Purpose

This packet gives a web-based ChatGPT durable, auditable context for the current Project Review System (PRS) work. It is navigation and recovery context only. Current repository files, current remote refs, applicable PRS procedures, and the user's current instructions always outrank it.

The user wants the local-first PRS design completed through governed review and an implementation-ready specification, then a hard stop before implementation. They are protective of the roadmap's architecture and requirements: do **not** casually rewrite or simplify its substantive design content merely to repair governance bookkeeping.

## Hard boundaries

- Do not implement the new local-first PRS engine, production controller/state/persistence code, migrations, production commands, or prototypes unless the user explicitly changes the stop-before-implementation boundary.
- Do not hard-reset, discard unrelated work, rewrite history, squash, or reinterpret historical evidence to obtain current credit.
- Do not treat a passing deterministic script as proof of semantic correctness, reviewer independence, or host-message/context separation.
- Do not treat this packet, a branch name, or newer commits as proof that review credit is current.
- Preserve revision-12, revision-13, and later evidence chronologically. If a correction invalidates credit, reopen according to current PRS rather than editing old evidence.
- The user asked the present Codex agent to stop before writing the artifact-identity implementation code. A different agent may analyze, propose, implement, or validate it only within the user's authority and current PRS procedure.

## Persistent goal authority

Read this first on every continuation:

`handoff-maintenance/project-review-system/CODEX_PERSISTENT_GOAL_TO_IMPLEMENTATION_BOUNDARY.md`

Its terminal condition is:

1. controller-core recovery validly complete;
2. local-first PRS design governed review/convergence complete; and
3. implementation-ready specification durably recorded.

Then stop before implementation.

The present remote `origin/main` at the time of this packet was:

`b400746115c7c5417a1bdb72fe38f6ee0743be32`

Remote:

`https://github.com/rpjgauthier-spec/project-review-system.git`

## Current worktree/ref map

These are locators, not authorities. Re-check them before use.

| Purpose | Ref / commit | State |
| --- | --- | --- |
| User's original checkout | `review-local-first-refactor-roadmap` at `1033376…` | User-owned, stale relative to remote and may be dirty. Do not reset or move it. |
| Current remote local-first roadmap | `origin/review-local-first-refactor-roadmap` at `a2769e09efe6836c449e4e20a5bfb4a2b205660d` | Current known design-review locator. |
| Controller-core recovery closure | `codex/recovery-pass-boundary-r13` at `ad07e3a619f92ed19a86b522cce947f7d6108ee0` | Local revision-14 recovery/evaluation closure. Not pushed. |
| Local-first revision-2 gate setup | `cc483b23e1089bdb1e4d09fcfb351e22b2e1cb07` | Valid committed gate setup; revision-2 Adversarial gate was created here. |
| Malformed attempted r2 completion | `codex/local-first-normalization` at `9f9cbfbe12595ca0730edd3bb734779b058696db` | Do not use as valid credit. It contains an immutable-ledger recording error. Preserve it; do not amend/reset it without explicit user authority. |
| Clean attempted r2 recovery | `codex/local-first-r2-recovery` based on `cc483b2` | Has uncommitted attempted completion state. Treat as disposable diagnostic work, not authority. |
| Prepared artifact-identity correction | `codex/git-blob-identity-recovery` based on `origin/review-local-first-refactor-roadmap` | Contains only an uncommitted change-impact record; no checker or test code changed. |

## What is complete and what is not

### Controller-core recovery

The bounded controller-core recovery reached a locally committed revision-14 closure at `ad07e3a`.

Verified at the time:

- revision-14 five semantic-stage results recorded;
- twelve required evaluations recorded with specific regression evidence;
- `update_revalidation_queue.py --check --base e192b19… --head HEAD` clear;
- pass-boundary, execution-identity-history, and changed-file coverage checks passed;
- PRS test suite: 109 tests passed;
- product tests: 27 passed with `PYTHONPATH=src`.

The correction preserved invalid revision-12 history as reservation evidence. It did **not** rewrite that history into valid credit.

### Local-first architecture

The remote branch has a rich design corpus and historical revision-1 roadmap review evidence. Do not assume it is current credit.

Authoritative design inputs to inspect:

- `skills/project-review-system/reviews/local-first-refactor-roadmap.md`
- `skills/project-review-system/reviews/local-first-refactor-roadmap-dogfood-gap.md`
- `skills/project-review-system/reviews/local-first-refactor-roadmap-normalization.md`
- `skills/project-review-system/reviews/local-first-refactor-roadmap-structural-optimization.md`
- `skills/project-review-system/reviews/local-first-refactor-roadmap-end-to-end.md`
- `skills/project-review-system/reviews/local-first-refactor-living-design-notes.md` — explicitly non-authoritative notebook; use as input only.

The roadmap's core design constraints include:

- local-first and deterministic-first operation; ordinary review must not require GitHub Actions or hosted quota;
- semantic judgment by a human/model versus deterministic state/eligibility owned by software;
- optional, least-privilege, provider-neutral retrieval/model integrations with manual fallback;
- user-owned provider installation, capability, and data-egress permission;
- canonical snapshot identity; stale snapshot/index/output rejection;
- atomic, concurrency-safe, replay-safe workflow state;
- migration that preserves PR6-era historical evidence without retroactive laundering;
- review breadth accounting and one authoritative owner for evaluation results;
- a reference direction of one workflow engine with SQLite as local transactional storage, thin adapters, generated views, Git/GitHub optional, and no large plug-in framework;
- no claim of local tamper-proofness/non-repudiation under a fully user-controlled machine.

The design is not an implementation authorization.

## Historic pass-boundary recovery

Revision-12 established evidence recorded an End-to-end handoff consumer as:

`End-to-end validation/contract-composition`

while the checker required:

`End-to-end validation:contract-composition`

That slash/colon mismatch is historical evidence. Do not edit revision-12 material to make a later validator pass.

Revision 14 corrected identity history handling so an invalid pre-existing base snapshot reserves occurrence/execution-unit/boundary identities without being treated as new current credit. The relevant code/history includes:

- `skills/project-review-system/scripts/check_execution_identity_history.py`
- `skills/project-review-system/tests/test_execution_identity_reopening.py`
- controller record: `skills/project-review-system/changes/2026-08-08-controller-core-skeleton.json`

## Current blocking defect: artifact-state identity is checkout-dependent

### Verified facts

`skills/project-review-system/scripts/check_execution_gate.py` currently calculates governed artifact identity by reading raw working-tree file bytes and deriving a Git-style blob SHA-1 locally. This makes the identity depend on line endings in the checkout.

With `core.autocrlf=true`, a clean Windows checkout produced a different target identity for the same committed local-first roadmap artifacts:

- recorded revision-2 gate target: `sha256:f1986f520aa5a218e423e23e97604b09447eaeea28f1af92f08d48913b409195`
- clean-checkout working-tree identity: `sha256:efcc49afa7c9c6987e1e554cbeea4fb6280e4eefa225c9d32dc8d04fcc02dd62`
- identity calculated from the committed Git blob IDs: `sha256:044e2dec0f57354228e08692475e3f7216987ab5249ffae371a47c6265a7a4f1`

This means a gate can become stale without a committed artifact change. Do not force it to pass by changing line endings, changing the recorded target, or reusing stale credit.

### Likely bounded correction surface

- `skills/project-review-system/scripts/check_execution_gate.py`
- `skills/project-review-system/tests/test_check_execution_gate.py`
- a new change-impact record already drafted but uncommitted at `skills/project-review-system/changes/2026-08-10-git-blob-artifact-identity.json`
- generated `skills/project-review-system/reviews/revalidation-queue.md`

The intended behavioral outcome is not merely “use HEAD.” A sound correction must define, test, and document all of these:

1. artifact identity is stable for the same committed Git blobs across checkout line-ending conversion;
2. absent governed paths remain representable and deterministic;
3. dirty or untracked governed files cannot silently receive a target identity derived from `HEAD` and then obtain credit for different bytes;
4. paths must remain repository-contained and ordinary Git failures must fail closed;
5. existing current-target/revision/gate/completion enforcement stays intact;
6. no historical record is rewritten to manufacture new credit.

Do not assume the only solution is one particular Git invocation. Compare alternatives against these invariants and the current PRS scope.

## Local-first review-credit issue

The roadmap's revision-1 record is:

`skills/project-review-system/changes/2026-08-08-local-first-refactor-roadmap-review.json`

It historically records completed stages, gates, completions, and ledger occurrences. When tested as a current branch record with `update_revalidation_queue.py --check --base <current-base> --head <head>`, its old gates were stale against the final governed artifact set.

The minimally correct response was to preserve revision-1 evidence and reopen revision 2, not to rewrite revision 1. The valid setup commit `cc483b2`:

- updates only the roadmap's displayed state/handoff, not its architecture;
- sets the record to `in_progress`, `review_revision: 2`;
- clears current live stage results/gates/completions while preserving the append-only revision-1 occurrence ledger;
- creates a new, validated revision-2 Adversarial gate;
- regenerates the queue.

The next semantic stage after a **valid** r2 Adversarial completion is Interdependency. Do not start it until current artifact identity and r2 credit are valid.

## Malformed r2 attempt: preserve, do not reuse

Commit `9f9cbfb` attempted to record the r2 Adversarial pass. Its `execution_occurrence_history[*].pass_evidence_sha256` was mistakenly assigned the handoff hash rather than the canonical hash of the entire completed pass object.

PRS correctly rejected this with an identity-history mutation/inconsistency error. A follow-up commit changing that ledger entry would itself violate append-only history. Do not amend, reset, or silently overwrite this commit unless the user explicitly authorizes history rewriting and current PRS authority allows it.

Prefer a new clean recovery ref and a fresh bounded execution after the artifact-identity control is corrected.

## Current PRS procedure and validation commands

Always read, at minimum:

- `skills/project-review-system/SKILL.md`
- `skills/project-review-system/references/shared-control-model.md`
- `skills/project-review-system/references/adaptive-execution.md`
- the exact current stage procedure before that stage.

Useful deterministic commands, with real base/head selected from current repository evidence:

```powershell
python skills/project-review-system/scripts/update_revalidation_queue.py
python skills/project-review-system/scripts/update_revalidation_queue.py --check --base <base-sha> --head <head-sha>
python skills/project-review-system/scripts/check_execution_identity_history.py --base <base-sha> --head <head-sha>
python skills/project-review-system/scripts/check_pass_boundaries.py
python skills/project-review-system/scripts/check_change_impact_coverage.py --base <base-sha> --head <head-sha>
python -m unittest discover -s skills/project-review-system/tests -p 'test_*.py'
```

For product tests in a source checkout:

```powershell
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -p 'test_*.py'
```

Expected caveat: `test_update_revalidation_queue.py` intentionally exercises a failure path that prints `ERROR: --check requires --base and --head`; the enclosing test suite can still pass.

## Recommended web-ChatGPT workflow

1. Treat this packet as a map, not authority. Re-fetch refs and inspect status/remote/branch/worktree state.
2. Preserve user-owned dirty work. Use a new clean worktree for any correction.
3. Read the persistent goal and current PRS modules.
4. Establish the actual PR base from repository/PR evidence; do not infer review continuity merely from commit order.
5. For the artifact-identity defect, determine the minimal correction design and classify it through a current change-impact record.
6. Before a semantic stage, create and validate the required Adaptive Execution gate and commit it first.
7. Perform exactly one bounded semantic stage per fresh execution boundary. Record completion, handoff, occurrence ledger, and validation before moving onward.
8. Keep correction code, review results, historical evidence, and generated queue state distinct.
9. Once PRS control recovery is valid, return to the local-first roadmap recovery at r2 Adversarial—not directly to Interdependency, Normalization, architecture changes, or implementation.
10. At the eventual design endpoint, produce a durable implementation-ready specification with contracts, states/transitions, persistence/recovery/concurrency, providers/trust, migration/portability, validation, and acceptance criteria. Stop before implementation.

## What a web ChatGPT may safely contribute

- Analyze repository evidence and current PRS authority.
- Compare correction alternatives and produce a design/review memo.
- Draft an implementation-ready specification or a change-impact proposal.
- Implement a narrowly authorized correction in a clean worktree if the user authorizes it, then run current PRS-required validation.
- Review another agent's patch for history preservation, Git portability, dirty-state safety, and revalidation consequences.

It must not claim that the local-first roadmap is validated simply because its old reports exist, or that a local deterministic check proves the semantic design is correct.

## Publication note

This packet was created on branch `codex/web-chatgpt-handoff` from `origin/main`. The local environment did not have GitHub CLI installed, so it could be committed locally but not safely pushed/opened as a PR through the configured publish workflow.
