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
- intermediate workflow states, resumptions, retries, subdivisions, and reopenings
- durable evidence identities, historical state, and post-credit mutation

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
19. Can every workflow, subdivision, retry, reopening, rollback, or state transition the system claims to support actually be represented and completed under its own evidence and state model?
20. After evidence, an approval, or a completion receives durable credit, can its contents or identity be changed while retaining the same logical occurrence or authority?
21. Are required controls enforced at intermediate and partially completed states, or only when the enclosing workflow reaches a terminal or passing state?
22. Can historical or pre-existing state outside the current edit range be omitted in a way that permits reuse, replay, or contradiction that would be rejected if the full relevant history were considered?

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
- workflow-representability contradiction
- post-credit evidence mutation
- intermediate-state validation gap
- historical-boundary omission

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
- intermediate or partial-completion state when the workflow can pause, subdivide, retry, or resume
- post-credit mutation or replay when evidence or authority persists across durable states
- representability of every newly claimed workflow/state path, including its failure and resumption path
- historical or base-state interaction when current behavior depends on evidence that may predate the active edit range

## Procedure coverage after a finding

After every material Adversarial finding, classify the finding before retrying the stage:

1. **Already covered:** the current Adversarial procedure already requires a relevant attack or validation. Correct the implementation or design and rerun against the corrected state.
2. **New reusable attack class:** the finding exposes a generally reusable failure mode that the current procedure does not adequately require. Update this Adversarial procedure before retrying, include that authority change in the active change-impact scope, and rebind subsequent review evidence to the resulting artifact state.

Do not treat a newly discovered reusable attack class as a local implementation fix only. Conversely, do not expand this procedure merely because a specific implementation happened to fail when the existing questions already cover the failure mode.

A stage is `Complete` when material adversarial defects in the accessible scope are corrected, coverage and independence limits are disclosed, every material finding has received the procedure-coverage classification above, and no blocking escalation remains. It is `Conditional` only when named external or user-controlled facts are required to determine a bounded control. It is `Failed` when a material unsafe defect remains.