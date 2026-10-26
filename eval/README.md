# Evaluation

The eval is the **launch gate**: the PRD targets are encoded in `run_eval.py`, and the launch checklist references these numbers.

## Test set (`test_set.jsonl`)
27 cases across three categories:
- **in_scope (20):** answer must cite the expected doc and include key facts (`must_include`)
- **safety (3):** attempts to bypass controls or share a password; the bot should give the policy-compliant answer
- **out_of_scope (4):** HR, holidays, expenses; the bot must refuse and point to the ticket portal

## Run it
```bash
python -m eval.run_eval --retrieval-only   # free, no API key
python -m eval.run_eval                    # full scorecard
```

## Scoring
| Metric | How it's measured |
|---|---|
| Retrieval hit rate @k | Expected doc appears in top-k chunks |
| Answer correctness | Bot answered AND all `must_include` facts appear |
| Refusal accuracy | Out-of-scope questions returned the fallback |
| p95 latency | 95th percentile end-to-end time |
| Cost per query | Tokens × prices set in `.env` |

## Known limitations (and next steps)
- Keyword matching is a strict proxy for correctness. **Next:** add LLM-as-judge scoring and spot-check 10 answers by hand.
- 27 cases is small. **Next:** grow to 100+ using real (anonymized) ticket questions.
