"""Unit tests — run without an API key."""
from src.ingest import load_chunks
from src.pipeline import FALLBACK, Pipeline
from src.retriever import Retriever


def test_docs_load_into_chunks():
    chunks = load_chunks()
    assert len(chunks) > 10
    assert all(c.source.endswith(".md") and c.text for c in chunks)


def test_vpn_question_retrieves_vpn_doc():
    hits = Retriever().search("How do I reset my VPN password?")
    assert hits and hits[0].chunk.source == "vpn.md"


def test_unrelated_question_triggers_guardrail():
    # A question sharing no vocabulary with the docs scores 0, so the guardrail returns the
    # fallback without calling the LLM (no API key needed). Near-miss out-of-scope questions
    # are handled by the LLM's NOT_FOUND rule — see ADR-002 findings.
    ans = Pipeline().ask("Who won the 1998 World Cup final?")
    assert not ans.answered
    assert ans.text == FALLBACK


def test_retrieval_hit_rate_meets_floor():
    """Regression guard: fail CI if a change tanks retrieval quality."""
    from eval.run_eval import run

    assert run(retrieval_only=True)["metrics"]["retrieval_hit_rate"] >= 0.80
