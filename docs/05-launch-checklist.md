# Launch Checklist (Go / No-Go)

Launch requires every **P0** item green. P1 items may launch with a documented plan.

## Quality — P0
- [ ] Answer correctness ≥ 85% on eval set
- [ ] Out-of-scope refusals = 100%
- [ ] Every answer includes at least one source citation
- [ ] Zero answers contradicting security policy

## Performance & cost — P0
- [ ] p95 latency < 4 s
- [ ] Cost per query < $0.01, monthly budget estimate approved

## Safety & compliance — P0
- [ ] Security review sign-off
- [ ] No credentials or PII in logs (verified)
- [ ] Escalation-to-ticket path tested

## Operations — P1
- [ ] Owner named for doc freshness
- [ ] Feedback (thumbs up/down) captured and reviewed weekly
- [ ] Rollback plan: disable bot link on ticket form
- [ ] Usage and cost alerts configured

## Comms — P1
- [ ] Announcement drafted for employees
- [ ] Support team briefed on how escalations arrive

## Decision

| Date | Decision | Approvers | Notes |
|---|---|---|---|
| _YYYY-MM-DD_ | _GO / NO-GO_ | _TPM, Eng lead, Security, IT lead_ | |
