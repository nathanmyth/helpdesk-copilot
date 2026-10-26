# ADR-002: Start with a TF-IDF retrieval baseline

**Status:** Accepted · **Date:** _YYYY-MM-DD_ · **Decider:** _Your name_

## Context
Retrieval choice affects quality, cost, and infrastructure. We don't yet know whether a simple approach is good enough for our doc set.

## Options
| Option | Pros | Cons |
|---|---|---|
| **A. TF-IDF keyword retrieval** | Zero cost, no API, runs in CI, transparent | Misses synonyms ("can't log in" vs "authentication failure") |
| B. Embeddings + vector DB | Handles paraphrase and synonyms | Embedding API cost, extra infrastructure |
| C. Hybrid (keyword + embeddings) | Best of both | Most complex |

## Decision
**Start with A as a measured baseline.** Upgrade to B or C only if the eval shows retrieval hit rate @3 below the 90% target.

## Consequences
- We get a baseline number before spending on infrastructure. This is the "measure, then invest" story.
- The retriever sits behind a small interface (`Retriever.search()`), so swapping it doesn't touch the pipeline.
## Findings from the baseline eval
- Retrieval hit rate @3: **100%** on the 23 in-scope and safety questions. Above target, so no embeddings upgrade needed yet.
- The similarity threshold alone **cannot** separate out-of-scope questions: "What is the company's parental leave *policy*?" scored 0.21, higher than real IT questions such as the browser-extension one (0.13).
- **Decision:** keep the threshold low (0.12) so real questions aren't dropped, and rely on the LLM's `NOT_FOUND` rule as a second guardrail layer. Refusal accuracy is measured in the full eval.

- **Follow-up:** after the M2 eval, record results here and either close this ADR or open ADR-004 for the upgrade.
