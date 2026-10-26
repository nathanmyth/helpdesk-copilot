"""TF-IDF retrieval baseline (see docs/decisions/ADR-002)."""
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src import config
from src.ingest import Chunk, load_chunks


@dataclass
class Hit:
    chunk: Chunk
    score: float


class Retriever:
    """Swap this class for an embeddings-based retriever without touching the pipeline."""

    def __init__(self, chunks: list[Chunk] | None = None):
        self.chunks = chunks if chunks is not None else load_chunks()
        if not self.chunks:
            raise ValueError(f"No documents found in {config.DOCS_DIR}")
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform(c.text for c in self.chunks)

    def search(self, query: str, k: int = config.TOP_K, min_score: float = config.MIN_SCORE) -> list[Hit]:
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0]
        ranked = scores.argsort()[::-1][:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in ranked if scores[i] >= min_score]
