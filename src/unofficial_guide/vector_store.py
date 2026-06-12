import json
import re
from pathlib import Path
from typing import Any, Iterable

from unofficial_guide.embeddings import Embedder
from unofficial_guide.models import RetrievedChunk, ReviewChunk


REQUIRED_METADATA = ("professor", "course", "source_url", "chunk_index")


class ChromaReviewStore:
    def __init__(
        self,
        client: object,
        collection_name: str,
        embedder: Embedder,
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.embedder = embedder
        self.collection = self.client.get_or_create_collection(name=collection_name)

    @classmethod
    def persistent(
        cls,
        path: Path | str,
        collection_name: str,
        embedder: Embedder,
    ) -> "ChromaReviewStore":
        import chromadb

        client = chromadb.PersistentClient(path=str(path))
        return cls(client, collection_name, embedder)

    @classmethod
    def in_memory(
        cls,
        collection_name: str,
        embedder: Embedder,
    ) -> "ChromaReviewStore":
        import chromadb

        client = chromadb.Client()
        return cls(client, collection_name, embedder)

    def rebuild(self, chunks: Iterable[ReviewChunk]) -> None:
        chunk_list = list(chunks)
        existing_collections = {
            getattr(collection, "name", str(collection))
            for collection in self.client.list_collections()
        }
        if self.collection_name in existing_collections:
            self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        if not chunk_list:
            return

        documents = [chunk.text for chunk in chunk_list]
        self.collection.add(
            ids=[make_chunk_id(chunk) for chunk in chunk_list],
            documents=documents,
            metadatas=[normalize_metadata(chunk.metadata) for chunk in chunk_list],
            embeddings=self.embedder.embed_texts(documents),
        )

    def query(
        self,
        query: str,
        top_k: int,
        where: dict[str, Any] | None = None,
    ) -> list[RetrievedChunk]:
        query = query.strip()
        if not query:
            raise ValueError("query cannot be empty")
        result = self.collection.query(
            query_embeddings=[self.embedder.embed_query(query)],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        return _flatten_query_result(result)

    def count(self) -> int:
        return int(self.collection.count())


def load_chunks_jsonl(path: Path) -> list[ReviewChunk]:
    chunks: list[ReviewChunk] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            chunks.append(_chunk_from_payload(payload, line_number))
    return chunks


def make_chunk_id(chunk: ReviewChunk) -> str:
    metadata = chunk.metadata
    parts = [
        _slug(str(metadata["professor"])),
        _slug(str(metadata["course"])),
        _slug(str(metadata.get("rating_id") or "rating")),
        _slug(str(metadata["chunk_index"])),
    ]
    return "-".join(part for part in parts if part)


def normalize_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    normalized: dict[str, str | int | float | bool] = {}
    for key, value in metadata.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        else:
            normalized[key] = str(value)
    professor = normalized.get("professor")
    course = normalized.get("course")
    if isinstance(professor, str):
        normalized["professor_normalized"] = professor.strip().lower()
    if isinstance(course, str):
        normalized["course_normalized"] = re.sub(r"\s+", "", course.upper())
    return normalized


def _chunk_from_payload(payload: object, line_number: int) -> ReviewChunk:
    if not isinstance(payload, dict):
        raise ValueError(f"line {line_number}: chunk must be a JSON object")
    text = payload.get("text")
    metadata = payload.get("metadata")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"line {line_number}: text is required")
    if not isinstance(metadata, dict):
        raise ValueError(f"line {line_number}: metadata is required")

    missing = [field for field in REQUIRED_METADATA if field not in metadata]
    if missing:
        raise ValueError(f"line {line_number}: missing metadata {', '.join(missing)}")
    return ReviewChunk(text=text, metadata=dict(metadata))


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _flatten_query_result(result: dict[str, Any]) -> list[RetrievedChunk]:
    documents = result.get("documents") or [[]]
    metadatas = result.get("metadatas") or [[]]
    distances = result.get("distances") or [[]]
    rows: list[RetrievedChunk] = []
    for text, metadata, distance in zip(documents[0], metadatas[0], distances[0]):
        rows.append(
            RetrievedChunk(
                text=text,
                metadata=dict(metadata or {}),
                distance=float(distance),
            )
        )
    return rows
