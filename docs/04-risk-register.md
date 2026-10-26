# Risk Register

Likelihood and Impact: **H**igh / **M**edium / **L**ow. Reviewed weekly.

| ID | Risk | L | I | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | **Hallucination:** bot gives a confident answer not supported by docs | M | H | Answer-only-from-context prompt; similarity threshold skips LLM when retrieval is weak; refusal cases in eval set | Eng | 🟡 Open |
| R-02 | **Unsafe guidance:** bot suggests bypassing a security control | L | H | Security-policy questions in eval set; Security review before launch | Security | 🟡 Open |
| R-03 | **Credential leakage:** users paste passwords into chat | M | H | UI warning; prompt never asks for credentials; logs exclude message bodies by default | Eng | 🟡 Open |
| R-04 | **Stale docs:** answers are correct to the doc but the doc is outdated | H | M | "Last updated" shown with sources; doc-owner review cadence agreed with IT Docs | IT Docs | 🟡 Open |
| R-05 | **Retrieval misses:** keyword retrieval fails on paraphrased questions | M | M | Measure hit rate @3 in M3; embeddings upgrade path ready (ADR-002) | Eng | 🟡 Open |
| R-06 | **Cost overrun:** usage exceeds budget | L | M | Cost per query tracked in eval; skip LLM on retrieval miss; usage alerts | TPM | 🟢 Monitoring |
| R-07 | **Vendor dependency:** API outage or pricing change | L | M | Model behind `src/llm.py` interface; fallback = link to ticket form | Eng | 🟢 Monitoring |
| R-08 | **Low adoption:** employees keep filing tickets | M | H | Link bot from ticket form; track deflection weekly; collect feedback | TPM | 🟡 Open |

## Closed risks
| ID | Risk | Resolution | Date |
|---|---|---|---|
| | | | |
