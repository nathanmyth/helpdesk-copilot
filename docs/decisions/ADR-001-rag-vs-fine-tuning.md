# ADR-001: Use RAG instead of fine-tuning

**Status:** Accepted · **Date:** _YYYY-MM-DD_ · **Decider:** _Your name_

## Context
We need an assistant that answers from IT documentation that changes weekly (new software, policy updates).

## Options
| Option | Pros | Cons |
|---|---|---|
| **A. RAG (retrieve docs at query time)** | Docs update instantly; answers can cite sources; no training cost | Quality depends on retrieval; more moving parts |
| B. Fine-tune a model on docs | Fast inference; no retrieval layer | Re-train on every doc change; can't cite sources; higher hallucination risk; training cost |
| C. Prompt with all docs in context | Simplest | Doesn't scale past a small doc set; cost grows with every query |

## Decision
**Option A (RAG).** Freshness and citations are P0 requirements (PRD R1, R2), and only RAG satisfies both.

## Consequences
- Retrieval quality becomes the main quality lever → measured separately in the eval (hit rate @3).
- Doc owners must keep source docs current; added to the risk register (R-04).
