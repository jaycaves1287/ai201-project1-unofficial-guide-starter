from unofficial_guide.generation import AnswerGenerator, GeneratedAnswer
from unofficial_guide.models import ReviewChunk
from unofficial_guide.retrieval import retrieve
from unofficial_guide.vector_store import ChromaReviewStore


NO_EVIDENCE_ANSWER = (
    "I do not have matching review chunks for that professor/course "
    "in the scraped RMP data."
)


def answer_question(
    query: str,
    store: ChromaReviewStore,
    chunks: list[ReviewChunk],
    generator: AnswerGenerator,
    top_k: int | None = None,
) -> GeneratedAnswer:
    query = query.strip()
    if not query:
        raise ValueError("query cannot be empty")

    retrieved_chunks = retrieve(query, store, chunks, top_k)
    if not retrieved_chunks:
        return GeneratedAnswer(answer=NO_EVIDENCE_ANSWER, citations=[])
    return generator.generate(query, retrieved_chunks)
