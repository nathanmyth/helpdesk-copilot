"""Settings loaded from environment variables (.env)."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # dotenv is optional
    pass

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = Path(os.getenv("DOCS_DIR", ROOT / "data" / "docs"))

LLM_MODEL = os.getenv("LLM_MODEL", "claude-haiku-5-5")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

TOP_K = int(os.getenv("TOP_K", "3"))
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.12"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))

# Pricing in USD per million tokens. Fill in from your provider's current pricing page.
PRICE_INPUT_PER_MTOK = float(os.getenv("PRICE_INPUT_PER_MTOK", "0"))
PRICE_OUTPUT_PER_MTOK = float(os.getenv("PRICE_OUTPUT_PER_MTOK", "0"))
