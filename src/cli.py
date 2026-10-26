"""Command-line interface.

    python -m src.cli "How do I reset my VPN password?"
    python -m src.cli --retrieve-only "How do I reset my VPN password?"
"""
import argparse

from src.retriever import Retriever


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask HelpDesk Copilot a question.")
    parser.add_argument("question")
    parser.add_argument("--retrieve-only", action="store_true", help="Show retrieved chunks; no LLM call.")
    args = parser.parse_args()

    retriever = Retriever()
    if args.retrieve_only:
        hits = retriever.search(args.question)
        if not hits:
            print("No relevant documents found (guardrail would trigger the fallback).")
        for h in hits:
            print(f"[{h.score:.2f}] {h.chunk.source} — {h.chunk.section}")
        return

    from src.pipeline import Pipeline

    ans = Pipeline(retriever).ask(args.question)
    print(ans.text)
    print(f"\n— {ans.latency_s:.2f}s · {ans.input_tokens}+{ans.output_tokens} tokens · ${ans.cost_usd:.5f}")


if __name__ == "__main__":
    main()
