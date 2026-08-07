# Evaluation: Identity Discovery

## Purpose

Test whether the reviewer can discover materially distinct identities without being given a candidate taxonomy, assuming a particular storage medium, or converting identity discovery into a restructuring recommendation.

## Scenario

A nontrivial body of work has accumulated over time. It may be stored in a repository, folder tree, document workspace, knowledge system, or another environment. No single authoritative statement resolves whether all material belongs to one coherent identity or to multiple materially distinct identities.

The reviewer is asked to perform a broad review. No candidate identities, expected layer count, project taxonomy, or environment-derived interpretation may be supplied as the expected result.

## Required behavior

A supported result requires all of the following:

1. Evidence is collected before identity labels are assigned.
2. The reviewer does not begin with a fixed checklist, seed taxonomy, presumed layer count, container-name interpretation, or prior expectation of what identities should exist.
3. Identities are inferred only from supported differences in purpose, lifecycle, authority, audience, artifact family, or delivery target.
4. Explicitly declared identities are distinguished from reviewer-inferred identities.
5. Shared material and overlaps may belong to multiple identities.
6. Material that cannot be assigned confidently remains uncertain or unassigned.
7. Multiple identities are not automatically treated as defects.
8. The reviewer does not recommend splitting, merging, moving, or reorganizing the storage environment merely because multiple identities were found.
9. Identity output is used as interpretation context for the five review stages rather than treated as a sixth stage or a new authority source.
10. Exhaustive identity claims use evidence appropriate to the reviewed environment; Git-specific exhaustive controls are used only for Git repository claims.

## Failure conditions

Fail this evaluation if the reviewer:

- searches for preselected identities or a preselected number of identities;
- forces every artifact into a predefined category;
- mistakes names, paths, folders, tags, or storage layout alone for semantic identity;
- silently treats an inferred identity as governing authority;
- equates multiple identities with a requirement to restructure storage;
- assumes Git-specific concepts are intrinsic to semantic identity discovery;
- skips identity ambiguity that materially affects later stage conclusions; or
- claims exhaustive identity discovery without evidence sufficient for the environment and claimed scope.