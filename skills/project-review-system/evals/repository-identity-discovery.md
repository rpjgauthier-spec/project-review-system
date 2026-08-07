# Evaluation: Repository Identity Discovery

## Purpose

Test whether the reviewer can discover materially distinct repository identities without being given a candidate taxonomy or converting the identity pass into a restructuring recommendation.

## Scenario

A repository contains a nontrivial collection of files created over time. The repository does not provide a single authoritative statement resolving whether all material belongs to one coherent project identity or to multiple materially distinct identities.

The reviewer is asked to perform a repository-wide review. No candidate identities, expected layer count, or project taxonomy may be supplied to the reviewer as part of the evaluation input.

## Required behavior

A supported result requires all of the following:

1. Evidence is collected before identity labels are assigned.
2. The reviewer does not begin with a fixed checklist, seed taxonomy, presumed layer count, repository-name interpretation, or prior expectation of what identities should exist.
3. Identities are inferred only from repository-supported differences in purpose, lifecycle, authority, audience, artifact family, or delivery target.
4. Explicitly declared identities are distinguished from reviewer-inferred identities.
5. Shared artifacts and overlaps may belong to multiple identities.
6. Material that cannot be assigned confidently remains uncertain or unassigned.
7. Multiple identities are not automatically treated as defects.
8. The reviewer does not recommend splitting, merging, or reorganizing the repository merely because multiple identities were found.
9. Identity output is used as interpretation context for the five review stages rather than treated as a sixth stage or a new authority source.
10. If the parent review is exhaustive, identity conclusions do not rely on search, sampling, or snippets as a substitute for the exhaustive semantic-coverage requirements.

## Failure conditions

Fail this evaluation if the reviewer:

- searches for preselected identities or a preselected number of identities;
- forces every file into a predefined category;
- mistakes directory or filename naming alone for semantic identity;
- silently treats an inferred identity as governing authority;
- equates multi-purpose repository structure with a requirement to split repositories;
- skips identity ambiguity that materially affects later stage conclusions; or
- claims exhaustive identity discovery without satisfying the parent exhaustive-coverage boundary.
