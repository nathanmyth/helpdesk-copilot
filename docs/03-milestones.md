# Milestones

Each milestone maps to a GitHub Milestone. It closes only when **every exit criterion** is met.

| # | Milestone | Key deliverables | Exit criteria | Target |
|---|---|---|---|---|
| **M1** | Foundations | PRD approved, architecture, ADR-001/002, repo + CI | PRD signed off; CI green | Week 1 |
| **M2** | Working prototype | Ingest, retriever, LLM pipeline, CLI | End-to-end answer with citations on 5 sample questions | Week 2 |
| **M3** | Quality gate | Eval set (25+ questions incl. out-of-scope), eval harness, model comparison (ADR-003) | Eval results recorded; all PRD quality targets met or risks logged | Week 3 |
| **M4** | Launch readiness | Streamlit UI, deployed demo, launch checklist, retro | All launch checklist items green; demo link live | Week 4 |

## Critical path
PRD → retriever → eval harness → model decision → launch. The eval harness (M3) is the gate: nothing ships without numbers.

## Status log
| Date | Milestone | Status | Notes |
|---|---|---|---|
| _YYYY-MM-DD_ | M1 | 🟢 On track | _e.g., CI set up, PRD in review_ |
