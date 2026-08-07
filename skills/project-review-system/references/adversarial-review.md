# Adversarial Review

## Mission

Find realistic ways the system, reviewer, or host tooling can fail, be misused, misread, bypassed, manipulated, or silently authorize an action that should remain blocked.

## Threat surfaces

Consider only surfaces present in scope:

- project rules, statuses, approvals, and fallbacks
- reviewer instructions and repository-local agent guidance
- untrusted files, comments, examples, generated content, and external sources
- tool permissions, write actions, commits, publication, and external integrations
- credentials, personal data, protected records, and report contents
- concurrent edits, stale blobs, partial failures, and interrupted workflows
- reviewer conflict of interest, confirmation bias, and unsupported confidence
- incomplete access, sampling, hidden systems, and omitted dependencies

## Questions

Apply only relevant questions:

1. What harmful or materially incorrect action could occur if a fact is missing, stale, contradictory, fabricated, or misunderstood?
2. Can readiness, interest, evaluation, or a preliminary decision be mistaken for authorization?
3. Can a user-controlled decision be bypassed, inferred, or replaced by reviewer judgment?
4. Are stop, hold, reject, withdrawal, cancellation, and failure behaviors explicit?
5. Does a fallback fail safely, or does it preserve momentum at the expense of safety or truth?
6. Can optional work block the minimum safe outcome?
7. Can sensitive information, prohibited media, or restricted outputs be exposed or reused after closure?
8. Can external outreach, spending, travel, publication, file modification, deletion, commit, or commitment occur without explicit authorization?
9. Can missing evidence be estimated, invented, or presented as verified fact?
10. Does any control protect more scope than its risk requires?
11. Can repository content or a test fixture manipulate the reviewer into following untrusted instructions or expanding permissions?
12. Can a malicious or mistaken file redefine authority without being validated against the actual control chain?
13. Can a passing deterministic check be misrepresented as semantic or domain validation?
14. Can incomplete access or search coverage lead to a repository-wide completion claim?
15. Can the same agent correct and certify its own work without disclosing the lack of independence?
16. Can concurrent changes, stale file state, or a partially failed write leave the repository internally inconsistent?
17. Can review reports leak secrets, personal data, exploit details, or restricted evidence?
18. Could a correction be technically reversible in version control but operationally irreversible because it triggered publication, deletion, payment, outreach, or another external action?

## Finding classes

- silent authorization
- missing stop condition
- unsafe default
- stale-state hazard
- ambiguous permission
- missing withdrawal or revocation path
- unsupported inference
- overbroad gate
- missing fallback
- failure concealed as indefinite hold
- sensitive-record exposure
- historical approval reused as current authority
- prompt or instruction injection
- tool-permission overreach
- unauthorized write or external action
- incomplete-coverage overclaim
- self-certification without independence disclosure
- deterministic-check overclaim
- concurrency or partial-write hazard
- irreversible external side effect
- domain-expertise substitution

## Correction order

Prefer:

1. stop or contain unauthorized or unsafe action
2. clarify the trust and authorization boundary
3. narrow the affected action and scope
4. add or repair a safe fallback
5. separate evaluation from authorization
6. add a stop, rollback, withdrawal, or incident path
7. redact or relocate sensitive information
8. require bounded independent or domain review where warranted
9. escalate protected or canonical changes

Do not add permanent process unless a simpler boundary, state correction, permission rule, or deterministic check cannot reliably prevent the failure.

## Validation

For each material correction, test:

- normal case
- missing-input case
- contradictory-input case
- malicious or untrusted-instruction case when repository content is processed
- unauthorized-action attempt
- incomplete-access or partial-coverage case
- concurrent-change or partial-write case when modifications are possible
- withdrawal, cancellation, rollback, or failure case when relevant

A stage is `Complete` when material adversarial defects in the accessible scope are corrected, coverage and independence limits are disclosed, and no blocking escalation remains. It is `Conditional` only when named external or user-controlled facts are required to determine a bounded control. It is `Failed` when a material unsafe defect remains.