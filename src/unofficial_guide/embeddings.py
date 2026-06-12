from typing import Protocol


class Embedder(Protocol):
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, query: str) -> list[float]:
        ...


class SentenceTransformerEmbedder:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        return _to_embedding_lists(embeddings)

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]


def _to_embedding_lists(embeddings: object) -> list[list[float]]:
    if hasattr(embeddings, "tolist"):
        return embeddings.tolist()
    return [list(embedding) for embedding in embeddings]  # type: ignore[union-attr]
