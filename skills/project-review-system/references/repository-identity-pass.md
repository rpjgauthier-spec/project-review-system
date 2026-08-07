# Repository Identity Pass

Run this pre-review pass for repository-wide or full-program review to determine whether materially distinct purposes coexist in one Git repository and whether those distinctions affect later review interpretation.

The pass is evidence-led. Do not seed candidate identities from user speculation, repository names, prior expectations, examples, or a fixed taxonomy. Collect evidence first; name identities only after the evidence supports them.

## Purpose

Determine whether the repository contains one coherent project identity or multiple materially distinct identities whose boundaries affect later review interpretation.

A repository identity is a coherent body of repository material with a distinguishable purpose, lifecycle, authority model, audience, artifact family, or delivery target. Multiple identities are not automatically defects and do not by themselves justify splitting a repository.

`Repository identity` in this module is a semantic project-interpretation concept. It is distinct from Git object identity, blob identity, commit identity, or other deterministic identifiers used by exhaustive coverage controls.

## Evidence collection

Before naming identities, inspect repository-wide evidence appropriate to the selected review depth. For an exhaustive review, use the pinned manifest and full-object processing requirements.

Collect signals such as:

- explicit purpose statements and scope declarations;
- authority and governance boundaries;
- artifact families and directory structure;
- lifecycle stages and completion criteria;
- producers, consumers, audiences, and delivery targets;
- naming conventions and vocabulary shifts;
- dependencies and cross-links between otherwise distinct clusters;
- contradictory or competing descriptions of what the repository is for.

Do not treat filename prefixes, directory names, repository names, or semantic search clusters as sufficient evidence by themselves.

## Discovery procedure

1. **Collect evidence without labels.** Record observations that may indicate distinct purposes or lifecycles before assigning identity names.
2. **Cluster only after evidence exists.** Group artifacts when multiple independent signals support a coherent purpose, lifecycle, authority, audience, artifact family, or delivery boundary.
3. **Separate explicit from inferred identity.** Mark identities explicitly declared by repository authorities separately from reviewer-inferred identities.
4. **Record overlap.** An artifact may support more than one identity. Shared material may legitimately span identities.
5. **Record unassigned material.** Do not force every artifact into an identity when evidence is insufficient. Preserve `unassigned` or `uncertain` status instead of guessing.
6. **Test materiality.** Retain an identity distinction only when it changes how later review stages should interpret authority, dependencies, normalization, structure, validation, or completion.
7. **Do not prescribe a split.** Repository separation, merging, archival, or restructuring is a later Structural Optimization question and requires its own evidence.

## Required output

For each discovered identity, record:

- a neutral descriptive name assigned after discovery;
- whether it is `explicit` or `inferred`;
- evidence supporting the identity;
- principal artifact families or representative paths;
- known authority or lifecycle boundary, when present;
- overlaps or shared material;
- confidence: `high`, `medium`, or `low`;
- material implications for later review stages.

Also record:

- unassigned or uncertain artifact groups;
- apparent identity conflicts or scope drift;
- whether the repository is adequately interpretable as a single identity;
- whether identity ambiguity blocks any later conclusion.

## Interaction with the five review stages

The Repository Identity Pass is not a sixth review stage and does not replace any stage.

Its output is interpretation context for:

- **Adversarial:** distinguish ambiguity, accidental authority transfer, stale project state, and unsafe cross-identity assumptions.
- **Interdependency:** identify real versus accidental dependencies and shared controls.
- **Normalization:** avoid normalizing intentionally different concepts that belong to different identities.
- **Structural Optimization:** evaluate whether overlap is justified, whether boundaries should be clarified, and only then whether restructuring is useful.
- **End-to-end validation:** select traces that cross material identity boundaries when such boundaries exist.

Identity findings never override repository authority. A reviewer-inferred identity is a hypothesis supported by evidence, not a new governing structure.

## Completion rule

The pass is complete when the reviewer can state one of the following with supporting evidence:

- no materially distinct repository identities were discovered;
- multiple materially distinct identities were discovered and their relevant boundaries are sufficiently characterized for the later stages; or
- identity ambiguity remains material and blocks specified downstream conclusions.

Do not claim repository identity exhaustiveness from search, sampling, or snippets when the parent review claims exhaustive repository coverage.
