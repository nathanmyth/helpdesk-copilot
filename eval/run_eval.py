"""Evaluation harness — the quality gate for launch.

    python -m eval.run_eval                  # full eval (needs API key)
    python -m eval.run_eval --retrieval-only # retrieval metrics only (free)

Writes eval/results/<timestamp>.json and prints a scorecard vs. PRD targets.
"""
import argparse
import json
import statistics
from datetime import datetime
from pathlib import Path

from src import config
from src.retriever import Retriever

HERE = Path(__file__).parent
TARGETS = {
    "retrieval_hit_rate": 0.90,
    "answer_correctness": 0.85,
    "refusal_accuracy": 1.00,
    "p95_latency_s": 4.0,
    "cost_per_query_usd": 0.01,
}


def load_cases() -> list[dict]:
    return [json.loads(line) for line in (HERE / "test_set.jsonl").read_text().splitlines() if line.strip()]


def p95(values: list[float]) -> float:
    if len(values) < 2:
        return values[0] if values else 0.0
    return statistics.quantiles(values, n=20)[-1]


def run(retrieval_only: bool) -> dict:
    cases = load_cases()
    retriever = Retriever()
    in_scope = [c for c in cases if c["expected_source"]]

    # Retrieval: does the expected doc appear in the top-k?
    hits = 0
    for c in in_scope:
        sources = {h.chunk.source for h in retriever.search(c["question"])}
        c["retrieval_hit"] = c["expected_source"] in sources
        hits += c["retrieval_hit"]
    metrics = {"retrieval_hit_rate": hits / len(in_scope)}

    if not retrieval_only:
        from src.pipeline import Pipeline

        pipe = Pipeline(retriever)
        correct = refused_ok = 0
        latencies, costs = [], []
        out_scope = [c for c in cases if not c["expected_source"]]

        for c in cases:
            ans = pipe.ask(c["question"])
            latencies.append(ans.latency_s)
            costs.append(ans.cost_usd)
            c["answer"] = ans.text
            if c["expected_source"]:
                ok = ans.answered and all(s.lower() in ans.text.lower() for s in c["must_include"])
                c["correct"] = ok
                correct += ok
            else:
                c["correct"] = not ans.answered
                refused_ok += not ans.answered

        metrics |= {
            "answer_correctness": correct / len(in_scope),
            "refusal_accuracy": refused_ok / len(out_scope) if out_scope else 1.0,
            "p95_latency_s": p95(latencies),
            "cost_per_query_usd": statistics.mean(costs),
        }

    return {"model": config.LLM_MODEL, "run_at": datetime.now().isoformat(timespec="seconds"),
            "metrics": metrics, "cases": cases}


def scorecard(metrics: dict) -> None:
    print(f"\n{'Metric':<22}{'Result':>10}{'Target':>10}   Status")
    print("-" * 52)
    for name, value in metrics.items():
        target = TARGETS[name]
        lower_is_better = name in ("p95_latency_s", "cost_per_query_usd")
        passed = value <= target if lower_is_better else value >= target
        fmt = (lambda v: f"{v:.1%}") if not lower_is_better else (lambda v: f"{v:.4g}")
        print(f"{name:<22}{fmt(value):>10}{fmt(target):>10}   {'✅ PASS' if passed else '❌ FAIL'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrieval-only", action="store_true")
    args = parser.parse_args()

    result = run(args.retrieval_only)
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(json.dumps(result, indent=2))

    scorecard(result["metrics"])
    misses = [c["id"] for c in result["cases"] if c.get("retrieval_hit") is False]
    if misses:
        print(f"\nRetrieval misses: {', '.join(misses)}")
    print(f"\nFull results: {out}")


if __name__ == "__main__":
    main()
