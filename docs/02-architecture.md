# Architecture

## Data flow

1. **Ingest** (`src/ingest.py`): load Markdown docs from `data/docs/`, split into ~500-character chunks with overlap, keep the source filename and section heading.
2. **Index** (`src/retriever.py`): build a TF-IDF index over chunks (baseline; see [ADR-002](decisions/ADR-002-retrieval-baseline.md)).
3. **Retrieve**: score the question against all chunks, return the top-k (default 3) above a minimum similarity threshold.
4. **Guardrail check** (`src/pipeline.py`): if nothing clears the threshold, return the escalation message *without calling the LLM* (saves cost, prevents hallucination).
5. **Generate** (`src/llm.py`): send the system prompt, retrieved chunks, and question to the LLM. The prompt instructs it to answer only from context and cite sources.
6. **Respond**: answer + cited sources + latency + token usage, shown in the Streamlit UI or CLI.

## Components

| Component | Choice (v1) | Swap path |
|---|---|---|
| Document store | Markdown files in repo | Confluence / SharePoint connector |
| Retriever | TF-IDF (scikit-learn) | Embeddings + vector DB (ADR-002) |
| LLM | Anthropic Claude via API, model set in `.env` | Any provider behind `src/llm.py` |
| UI | Streamlit | Slack bot / Teams app |
| Eval | `eval/run_eval.py` + JSONL test set | Add LLM-as-judge scoring |

## Non-functional requirements

- **Latency:** retrieval < 100 ms; end-to-end p95 < 4 s
- **Privacy:** no PII in logs; no credentials in prompts or responses
- **Cost:** retrieval is local and free; LLM called only when retrieval succeeds
- **Observability:** every response returns latency and token counts for the eval harness
