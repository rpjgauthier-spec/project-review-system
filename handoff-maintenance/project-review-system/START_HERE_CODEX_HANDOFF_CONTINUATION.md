# START HERE — Codex Handoff Maintenance Continuation

## Purpose

Use this file to continue the current Project Review System Codex-handoff maintenance work in a fresh ChatGPT conversation without relying on prior chat history.

Repository: `rpjgauthier-spec/project-review-system`

This directory maintains and reviews the Codex recovery handoff. It is not Project Review System production authority and is intentionally outside `skills/project-review-system/**` so routine handoff maintenance does not itself enter the PRS changed-file/revalidation surface.

## Current artifacts

- Recovery handoff: `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md`
- Maintenance guide: `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`
- Mandatory pre-review method: `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`
- Adversarial stage model: `CODEX_HANDOFF_ADVERSARIAL_REVIEW_MODEL.md`
- Interdependency stage model: `CODEX_HANDOFF_INTERDEPENDENCY_REVIEW_MODEL.md`
- Normalization stage model: `CODEX_HANDOFF_NORMALIZATION_REVIEW_MODEL.md`
- Structural Optimization stage model: `CODEX_HANDOFF_STRUCTURAL_OPTIMIZATION_REVIEW_MODEL.md`
- End-to-end stage model: `CODEX_HANDOFF_END_TO_END_REVIEW_MODEL.md`
- Stage-model meta-audit: `CODEX_HANDOFF_STAGE_MODEL_COMPLETENESS_AUDIT.md`

Only the current Lean handoff remains in the live maintenance directory. Superseded Lean revisions are retained by Git history, not as parallel canonical-looking files.

## Mandatory read order for future handoff maintenance

1. Read this file.
2. Read `CODEX_HANDOFF_MAINTENANCE_GUIDE.md`.
3. Read `CODEX_HANDOFF_MODEL_BEFORE_REVIEW.md`.
4. Read the applicable strengthened stage model.
5. Read `CODEX_HANDOFF_PROJECT_REVIEW_SYSTEM_LEAN_v9.md` when the review targets Lean.
6. Derive the bounded target-specific coverage witness required by Model Before Review and the stage model.
7. Complete and close the declared semantic sweep before reporting.
8. Ownership-Test blocker/high candidates before proposing corrections.
9. Before any nontrivial owned correction, perform Model Before Change and Structural Optimization / survive-or-die.

## Current status

**Lean v9 is converged and has been successfully used as the Codex recovery handoff.**

The maintenance method and all five stage maps were strengthened with bounded target-derived coverage closure. Lean v9 was then re-evaluated through separated semantic stages.

Initial strengthened-stage results:

- Adversarial: converged, zero blocker/high handoff-owned survivors.
- Interdependency: converged, zero blocker/high handoff-owned survivors.
- Normalization: converged, zero blocker/high handoff-owned survivors.
- Structural Optimization: converged, zero blocker/high handoff-owned survivors.

A later discoverability check found that the local-first roadmap and living design notes were not deterministically reachable from Lean alone. Repository inspection established their current known navigation location on branch `review-local-first-refactor-roadmap`:

- `skills/project-review-system/reviews/local-first-refactor-roadmap.md`
- `skills/project-review-system/reviews/local-first-refactor-living-design-notes.md`

Lean was minimally corrected to add those navigation pointers while requiring current location/applicability to be verified and preserving their non-authoritative relationship to repository/PRS authority.

Lean pointer-correction commit:

`5b6fa7839534508c6dca97e72e8350d37751b000`

Current Lean blob:

`db4e5295b91b5566bbba108d11d0b46300074a55`

The correction was then revalidated through the affected earlier lenses as separate execution boundaries:

- Delta Adversarial: converged, zero blocker/high handoff-owned survivors.
- Delta Interdependency: converged, zero blocker/high handoff-owned survivors.
- Delta Normalization: converged, zero blocker/high handoff-owned survivors.
- Delta Structural Optimization: converged, zero blocker/high handoff-owned survivors; the navigation block survived intact.

Full strengthened End-to-end validation then traced all materially reachable recovery journeys, interruption/re-entry classes, terminal contracts, and journey × terminal combinations, including the roadmap/living-notes discovery path.

End-to-end result:

- zero blockers;
- zero HIGH handoff-owned survivors;
- reachable journey × terminal/interruption inventory closed;
- terminal-report contracts closed;
- no Lean correction required.

Therefore the current Lean v9 handoff has converged under all five strengthened stage maps.

## Deployment result

The handoff was exercised in Codex against the actual repository state.

Codex correctly:

- verified the local checkout and remote refs without discarding dirty/diverged local work;
- recovered current repository/PRS/source-scope authority;
- reproduced the durable revision-12 `pass-boundary-enforcement` defect without rewriting historical evidence;
- reopened governed recovery at revision 13;
- durably completed revision-13 Adversarial and Interdependency as separate semantic execution boundaries;
- verified that no additional backward-impact, delta-review, or reopening obligation remained before the ordinary forward chain resumed.

Current known governed recovery state from that exercised handoff:

- revision 13 remains `in_progress`;
- Adversarial: current and durably complete;
- Interdependency: current and durably complete;
- next permitted semantic activity: Normalization, subject to re-establishing current repository/PRS state at execution time.

The successful deployment means no additional handoff semantic review is required unless the handoff itself changes or execution exposes a new handoff-owned defect.

## Exact next action

Continue the governed work from durable repository state using Codex Goal-mode continuations rather than creating a new handoff-maintenance revision.

The intended work horizon is:

1. finish the remaining governed controller-core recovery under current PRS authority;
2. finish the remaining reviewed local-first PRS architecture/design work, including any required corrections, reopenings, or revalidation;
3. produce and durably record an implementation-ready specification for the local deterministic PRS system;
4. **STOP BEFORE IMPLEMENTATION.**

The new local deterministic PRS engine is intentionally outside the Codex goal at this stage. Codex must not implement the engine, persistence backend, migration/cutover code, production commands, implementation skeleton, or implementation-driven test/debug cycle. A separate implementation step will build the reviewed deterministic program and later return it to the repository for governed validation and real-world dogfooding.

At every continuation, current repository and PRS authority outrank this navigation manifest. Do not force the historical stage sequence if current durable state has changed.

## Persistent Codex Goal boundary

The persistent Codex goal should:

- derive each next activity from current durable repository/PRS state;
- preserve required semantic execution boundaries rather than simulating them inside one execution;
- make required pre-semantic state durable before semantic work and make semantic completion durable before downstream credit;
- preserve historical evidence and follow reopening/revalidation when corrections invalidate prior credit;
- continue deterministic/non-semantic work automatically when current PRS permits it;
- finish the controller-core recovery and remaining local-first design review;
- stop once the reviewed design has converged and an implementation-ready specification is durably recorded;
- not cross into implementation of the new local deterministic engine.

## Pending Goal-prompt finalization

The persistent `/goal` execution contract is **not yet finalized for use**.

The most recent full Goal prompt was adversarially reviewed after the stop-before-implementation boundary was added. That review found three material prompt risks that still require the requested cull-the-herd / survive-or-die pass before the prompt should be treated as final:

1. the descriptive work checklist could accidentally become a second authority instead of remaining subordinate/disposable relative to current repository/PRS state;
2. the requested implementation-ready specification could drift into implementation-by-proxy (production code, executable pseudocode, concrete implementation bodies, migration scripts, or file-by-file coding instructions);
3. progress pressure needs an explicit fail-closed priority when continued advancement conflicts with uncertainty about authority, review credit, or semantic-boundary validity.

The next maintenance-chat task is therefore:

**Perform the cull-the-herd / survive-or-die review of the adversarially reviewed full persistent Goal prompt, produce the final reduced Goal prompt, and only then hand that prompt to Codex.**

Do not reopen Lean v9 semantic review merely to finalize this deployment prompt; this is Goal-prompt/deployment bookkeeping unless the resulting prompt change exposes a new Lean handoff-owned defect.

## Fresh maintenance-chat prompt

> In `rpjgauthier-spec/project-review-system`, read `handoff-maintenance/project-review-system/START_HERE_CODEX_HANDOFF_CONTINUATION.md` and every file it marks mandatory. Continue from the exact next action. Do not reopen handoff semantic review unless the handoff changed or a new handoff-owned defect was exposed.

## Update rule

Update this manifest whenever the current handoff version, maintenance method/model, review stage, convergence state, deployment result, or exact next action changes.
