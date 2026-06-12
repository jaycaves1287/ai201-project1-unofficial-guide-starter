import json
from pathlib import Path
from typing import Iterable

from unofficial_guide.chunking import chunk_ratings
from unofficial_guide.ingest import extract_ratings_from_store, extract_relay_store, fetch_html
from unofficial_guide.models import ProfessorSource, ReviewChunk


def build_chunks_from_html(source: ProfessorSource, html: str) -> list[ReviewChunk]:
    store = extract_relay_store(html)
    ratings = extract_ratings_from_store(store)
    return chunk_ratings(source, ratings)


def build_chunks_for_sources(
    sources: Iterable[ProfessorSource],
) -> list[ReviewChunk]:
    chunks: list[ReviewChunk] = []
    for source in sources:
        html = fetch_html(source)
        chunks.extend(build_chunks_from_html(source, html))
    return chunks


def write_chunks_jsonl(chunks: Iterable[ReviewChunk], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk.to_json(), ensure_ascii=True) + "\n")
