# Identity Pass

Run this pre-review pass when a broad or full-program review could be materially affected by multiple overlapping purposes, projects, workstreams, frameworks, experiments, templates, migrations, generated layers, or other distinct bodies of work sharing the reviewed scope.

The pass is evidence-led and medium-independent. Do not seed candidate identities from user speculation, workspace or repository names, prior expectations, examples, directory structure, or a fixed taxonomy. Collect evidence first; name identities only after the evidence supports them.

## Purpose

Determine whether the reviewed scope is adequately interpretable as one coherent identity or contains multiple materially distinct identities whose boundaries affect later review interpretation.

An identity is a coherent body of material with a distinguishable purpose, lifecycle, authority model, audience, artifact family, or delivery target. Multiple identities are not automatically defects and do not by themselves justify splitting, merging, moving, or reorganizing the underlying storage or workspace.

Identity in this module is a semantic interpretation concept. It is distinct from Git object identity, filesystem identity, database identifiers, document IDs, or other deterministic identifiers used by environment-specific evidence controls.

## Evidence collection

Before naming identities, inspect evidence appropriate to the selected review depth and environment. Collect signals such as:

- explicit purpose statements and scope declarations;
- authority and governance boundaries;
- artifact families and organization;
- lifecycle stages and completion criteria;
- producers, consumers, audiences, and delivery targets;
- vocabulary or naming shifts when corroborated by semantic evidence;
- dependencies and cross-links between otherwise distinct clusters;
- contradictory or competing descriptions of what the reviewed scope is for.

Do not treat names, paths, folders, tags, file prefixes, repository names, workspace names, or search clusters as sufficient evidence by themselves.

## Discovery procedure

1. **Collect evidence without labels.** Record observations that may indicate distinct purposes or lifecycles before assigning identity names.
2. **Cluster only after evidence exists.** Group material when multiple independent signals support a coherent purpose, lifecycle, authority, audience, artifact family, or delivery boundary.
3. **Separate explicit from inferred identity.** Mark identities explicitly declared by controlling authorities separately from reviewer-inferred identities.
4. **Record overlap.** Material may support more than one identity. Shared governance, infrastructure, templates, evidence, or services may legitimately span identities.
5. **Record unassigned material.** Do not force every artifact into an identity when evidence is insufficient. Preserve `unassigned` or `uncertain` instead of guessing.
6. **Test materiality.** Retain an identity distinction only when it changes how later review stages should interpret authority, dependencies, normalization, structure, validation, or completion.
7. **Do not prescribe restructuring from identity alone.** Separation, merging, archival, relocation, or restructuring is a later Structural Optimization question and requires its own evidence.

## Required output

For each discovered identity, record:

- a neutral descriptive name assigned after discovery;
- whether it is `explicit` or `inferred`;
- evidence supporting the identity;
- principal artifact families or representative locations;
- known authority or lifecycle boundary, when present;
- overlaps or shared material;
- confidence: `high`, `medium`, or `low`;
- material implications for later review stages.

Also record unassigned or uncertain material, apparent identity conflicts or scope drift, whether the reviewed scope is adequately interpretable as a single identity, and whether identity ambiguity blocks any later conclusion.

## Environment-specific evidence profiles

The Identity Pass does not define how an environment proves exhaustive coverage. Use the strongest applicable evidence mechanism for the environment being reviewed.

For a Git repository under an exhaustive repository claim, use the existing pinned-commit manifest, Git object identity, full-object processing, coverage ledger, and `check_review_coverage.py`. Those Git-specific controls remain repository-specific evidence machinery; they are not part of the Identity Pass abstraction itself.

For other environments, do not claim exhaustive identity discovery unless that environment has an evidence mechanism sufficient to support the claimed scope. State the limitation instead of borrowing Git-specific guarantees.

## Interaction with the five review stages

The Identity Pass is not a sixth review stage and does not replace any stage. Its output is interpretation context for:

- **Adversarial:** distinguish ambiguity, accidental authority transfer, stale state, and unsafe cross-identity assumptions.
- **Interdependency:** identify real versus accidental dependencies and shared controls.
- **Normalization:** avoid normalizing intentionally different concepts that belong to different identities.
- **Structural Optimization:** evaluate whether overlap is justified, whether boundaries should be clarified, and only then whether restructuring is useful.
- **End-to-end validation:** select traces that cross material identity boundaries when such boundaries exist.

Identity findings never override controlling authority. A reviewer-inferred identity is a hypothesis supported by evidence, not a new governing structure.

## Completion rule

The pass is complete when the reviewer can state one of the following with supporting evidence:

- no materially distinct identities were discovered;
- multiple materially distinct identities were discovered and their relevant boundaries are sufficiently characterized for later stages; or
- identity ambiguity remains material and blocks specified downstream conclusions.

Do not claim identity exhaustiveness from search, sampling, snippets, or naming patterns when the parent review claims exhaustive coverage.