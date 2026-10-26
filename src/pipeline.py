"""Retrieve → guardrail → prompt → answer."""
import time
from dataclasses import dataclass, field

from src import llm
from src.retriever import Hit, Retriever

FALLBACK = (
    "I couldn't find this in the IT knowledge base. "
    "Please file a ticket at the IT Service Portal and a support engineer will help."
)

SYSTEM_PROMPT = """You are HelpDesk Copilot, an IT support assistant for employees.

Rules:
- Answer ONLY using the context documents provided. If the answer is not in the context, reply exactly: "NOT_FOUND".
- Be concise: short steps or 2-4 sentences.
- End with "Sources:" followed by the document names you used.
- Never ask for, repeat, or store passwords, MFA codes, or other credentials.
- Never suggest bypassing a security control."""


@dataclass
class Answer:
    text: str
    sources: list[str] = field(default_factory=list)
    hits: list[Hit] = field(default_factory=list)
    answered: bool = True
    latency_s: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0


def build_context(hits: list[Hit]) -> str:
    return "\n\n".join(
        f"[Document: {h.chunk.source} — {h.chunk.section}]\n{h.chunk.text}" for h in hits
    )


class Pipeline:
    def __init__(self, retriever: Retriever | None = None):
        self.retriever = retriever or Retriever()

    def ask(self, question: str) -> Answer:
        start = time.perf_counter()
        hits = self.retriever.search(question)

        # Guardrail: no relevant docs → don't call the LLM at all.
        if not hits:
            return Answer(FALLBACK, answered=False, latency_s=time.perf_counter() - start)

        user = f"Context documents:\n\n{build_context(hits)}\n\nEmployee question: {question}"
        completion = llm.complete(SYSTEM_PROMPT, user)
        answered = "NOT_FOUND" not in completion.text
        sources = sorted({h.chunk.source for h in hits})

        return Answer(
            text=completion.text if answered else FALLBACK,
            sources=sources if answered else [],
            hits=hits,
            answered=answered,
            latency_s=time.perf_counter() - start,
            input_tokens=completion.input_tokens,
            output_tokens=completion.output_tokens,
            cost_usd=completion.cost_usd,
        )
