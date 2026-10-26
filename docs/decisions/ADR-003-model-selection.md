# ADR-003: Model selection

**Status:** Proposed · **Date:** _YYYY-MM-DD_ · **Decider:** _Your name_

## Context
The model drives answer quality, latency, and cost. Helpdesk answers are short and grounded in retrieved text, so a mid-size or small model may be enough.

## Evaluation plan
Run `eval/run_eval.py` against 2–3 candidate models (set `LLM_MODEL` in `.env`), holding the retriever and prompt constant.

| Model | Correctness | Refusal accuracy | p95 latency | Cost / query |
|---|---|---|---|---|
| _Large model_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| _Mid model_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| _Small model_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

## Decision rule
Pick the **cheapest model that meets every quality target** in the PRD. If none does, pick the best performer and log the cost overrun as a risk.

## Decision
_Fill in after running the eval._
