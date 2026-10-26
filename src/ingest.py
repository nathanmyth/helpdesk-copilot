"""Load Markdown documents and split them into section-aware chunks."""
from dataclasses import dataclass
from pathlib import Path

from src import config


@dataclass
class Chunk:
    text: str
    source: str   # filename
    section: str  # nearest heading


def _split_sections(text: str) -> list[tuple[str, str]]:
    """Split Markdown into (heading, body) pairs."""
    sections, heading, lines = [], "Introduction", []
    for line in text.splitlines():
        if line.startswith("#"):
            if any(l.strip() for l in lines):
                sections.append((heading, "\n".join(lines).strip()))
            heading, lines = line.lstrip("#").strip(), []
        else:
            lines.append(line)
    if any(l.strip() for l in lines):
        sections.append((heading, "\n".join(lines).strip()))
    return sections


def _split_long(body: str, size: int) -> list[str]:
    """Split a long section on paragraph boundaries so chunks stay under `size`."""
    parts, current = [], ""
    for para in body.split("\n\n"):
        if current and len(current) + len(para) > size:
            parts.append(current.strip())
            current = ""
        current += para + "\n\n"
    if current.strip():
        parts.append(current.strip())
    return parts


def load_chunks(docs_dir: Path = config.DOCS_DIR, size: int = config.CHUNK_SIZE) -> list[Chunk]:
    chunks = []
    for path in sorted(Path(docs_dir).glob("*.md")):
        for heading, body in _split_sections(path.read_text(encoding="utf-8")):
            for piece in _split_long(body, size):
                # Prefix the heading so it contributes to retrieval.
                chunks.append(Chunk(text=f"{heading}\n{piece}", source=path.name, section=heading))
    return chunks
