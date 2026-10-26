"""Thin model client. Replace the body of `complete` to use another provider."""
from dataclasses import dataclass

from src import config


@dataclass
class Completion:
    text: str
    input_tokens: int
    output_tokens: int

    @property
    def cost_usd(self) -> float:
        return (
            self.input_tokens * config.PRICE_INPUT_PER_MTOK
            + self.output_tokens * config.PRICE_OUTPUT_PER_MTOK
        ) / 1_000_000


def complete(system: str, user: str, model: str = config.LLM_MODEL, max_tokens: int = 500) -> Completion:
    if not config.ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")

    import anthropic  # imported lazily so retrieval-only runs don't need it

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(block.text for block in resp.content if block.type == "text")
    return Completion(text, resp.usage.input_tokens, resp.usage.output_tokens)
