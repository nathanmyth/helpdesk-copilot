# PRD: HelpDesk Copilot

| | |
|---|---|
| **Owner** | _Your name_ (TPM) |
| **Status** | Draft → In review → **Approved** → Shipped |
| **Last updated** | _YYYY-MM-DD_ |

## 1. Problem

Tier-1 IT tickets are dominated by repeat questions whose answers already exist in documentation (VPN, password resets, software requests, device setup). Employees can't find the docs; support engineers spend time re-answering.

**Evidence** _(replace with real or realistic numbers)_:
- ~40% of monthly tickets are tier-1 "how do I" questions
- Median time-to-resolution for these: 6 hours (mostly queue time)
- Each ticket costs ~15 minutes of engineer time

## 2. Users

| Persona | Need |
|---|---|
| **Employee** | Fast, trustworthy answer without filing a ticket |
| **IT support engineer** | Fewer repetitive tickets; escalations arrive with context |
| **IT/Security lead** | Assurance the bot won't give wrong or unsafe guidance |

## 3. Goals & success metrics

| Type | Metric | Target |
|---|---|---|
| **North star** | Tier-1 ticket deflection | 30% within 60 days of launch |
| Quality | Answer correctness on eval set | ≥ 85% |
| Quality | Out-of-scope questions correctly refused | 100% |
| Trust | Answers that cite a source doc | 100% |
| Experience | p95 latency | < 4 s |
| Cost | Cost per query | < $0.01 |
| **Guardrail** | Answers that contradict security policy | 0 |

## 4. Scope

**In scope (v1)**
- Q&A over IT knowledge-base documents
- Source citations on every answer
- "I don't know — here's how to file a ticket" fallback
- Thumbs up/down feedback

**Non-goals (v1)**
- Taking actions (resetting passwords, provisioning access)
- Personal account data lookups
- Languages other than English
- Replacing tier-2/3 support

## 5. Requirements

| ID | Requirement | Priority |
|---|---|---|
| R1 | Answer only from retrieved documents; refuse otherwise | P0 |
| R2 | Cite source document(s) for every answer | P0 |
| R3 | Never request or echo passwords/credentials | P0 |
| R4 | Escalation path to a human ticket | P0 |
| R5 | Log question, retrieved docs, latency, and feedback (no PII) | P1 |
| R6 | Model and retriever swappable via config | P1 |

## 6. Dependencies

- Knowledge-base owners keep docs current (IT Docs team)
- LLM API access and budget approval (Finance)
- Security review sign-off (Security)

## 7. Open questions

- Who owns doc freshness after launch?
- Do we route low-confidence answers straight to a ticket, or show them with a warning?
- What retention policy applies to query logs?
