from dataclasses import dataclass
from typing import Protocol

from unofficial_guide.models import RetrievedChunk


@dataclass(frozen=True)
class Citation:
    index: int
    professor: str
    course: str
    source_url: str
    rating_id: str
    date: str


@dataclass(frozen=True)
class GeneratedAnswer:
    answer: str
    citations: list[Citation]


class AnswerGenerator(Protocol):
    def generate(self, query: str, chunks: list[RetrievedChunk]) -> GeneratedAnswer:
        ...


def build_context(chunks: list[RetrievedChunk]) -> str:
    blocks: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk.metadata
        blocks.append(
            "\n".join(
                [
                    f"[{index}]",
                    f"Professor: {_metadata_text(metadata, 'professor')}",
                    f"Course: {_metadata_text(metadata, 'course')}",
                    f"Source: {_metadata_text(metadata, 'source_url')}",
                    f"Rating ID: {_metadata_text(metadata, 'rating_id')}",
                    f"Date: {_metadata_text(metadata, 'date')}",
                    f"Review: {chunk.text}",
                ]
            )
        )
    return "\n\n".join(blocks)


def build_messages(query: str, chunks: list[RetrievedChunk]) -> list[dict[str, str]]:
    context = build_context(chunks)
    return [
        {
            "role": "system",
            "content": (
                "Answer only from the provided review chunks. "
                "Use citations like [1] or [2] for claims. "
                "Do not invent professors, courses, ratings, grades, or student opinions. "
                "If the chunks do not answer the question, say there is not enough "
                "matching review evidence. Keep the answer short and student-friendly."
            ),
        },
        {
            "role": "user",
            "content": f"Question: {query}\n\nReview chunks:\n{context}",
        },
    ]


def citations_from_chunks(chunks: list[RetrievedChunk]) -> list[Citation]:
    return [
        Citation(
            index=index,
            professor=_metadata_text(chunk.metadata, "professor"),
            course=_metadata_text(chunk.metadata, "course"),
            source_url=_metadata_text(chunk.metadata, "source_url"),
            rating_id=_metadata_text(chunk.metadata, "rating_id"),
            date=_metadata_text(chunk.metadata, "date"),
        )
        for index, chunk in enumerate(chunks, start=1)
    ]


def format_answer_for_cli(answer: GeneratedAnswer) -> str:
    lines = ["Answer:", answer.answer, "", "Sources:"]
    if not answer.citations:
        lines.append("No sources returned.")
        return "\n".join(lines)

    for citation in answer.citations:
        lines.append(
            f"[{citation.index}] {citation.professor} - "
            f"{citation.course} - {citation.source_url}"
        )
    return "\n".join(lines)


class GroqAnswerGenerator:
    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.3-70b-versatile",
    ) -> None:
        if not api_key.strip():
            raise ValueError("GROQ_API_KEY is required")
        from groq import Groq

        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, query: str, chunks: list[RetrievedChunk]) -> GeneratedAnswer:
        if not chunks:
            return GeneratedAnswer(
                answer=(
                    "I do not have matching review chunks for that professor/course "
                    "in the scraped RMP data."
                ),
                citations=[],
            )

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=build_messages(query, chunks),
            temperature=0.2,
        )
        answer = completion.choices[0].message.content or ""
        return GeneratedAnswer(
            answer=answer.strip(),
            citations=citations_from_chunks(chunks),
        )


def _metadata_text(metadata: dict[str, object], key: str) -> str:
    value = metadata.get(key)
    if value is None or value == "":
        return "N/A"
    return str(value)
