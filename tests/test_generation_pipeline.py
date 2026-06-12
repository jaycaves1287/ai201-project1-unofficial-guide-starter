import pytest

from unofficial_guide.answering import answer_question
from unofficial_guide.generation import (
    GeneratedAnswer,
    build_context,
    build_messages,
    citations_from_chunks,
    format_answer_for_cli,
)
from unofficial_guide.models import RetrievedChunk, ReviewChunk


def sample_retrieved_chunks():
    return [
        RetrievedChunk(
            text="Professor: Alexander Rudnick\nCourse: CSE142\nReview: Great lectures.",
            metadata={
                "professor": "Alexander Rudnick",
                "course": "CSE142",
                "source_url": "https://example.com/rudnick",
                "rating_id": "111",
                "date": "2026-01-01",
            },
            distance=0.25,
        ),
        RetrievedChunk(
            text="Professor: Alexander Rudnick\nCourse: CSE13\nReview: Helpful examples.",
            metadata={
                "professor": "Alexander Rudnick",
                "course": "CSE13",
                "source_url": "https://example.com/rudnick",
                "rating_id": "222",
                "date": "2026-03-09",
            },
            distance=0.4,
        ),
    ]


def sample_review_chunks():
    return [
        ReviewChunk(
            text=chunk.text,
            metadata=dict(chunk.metadata, chunk_index=index),
        )
        for index, chunk in enumerate(sample_retrieved_chunks())
    ]


class FakeStore:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def query(self, query, top_k, where=None):
        self.calls.append({"query": query, "top_k": top_k, "where": where})
        return self.results


class FakeGenerator:
    def __init__(self):
        self.calls = []

    def generate(self, query, chunks):
        self.calls.append({"query": query, "chunks": chunks})
        return GeneratedAnswer(
            answer="Students say Rudnick is clear and helpful. [1]",
            citations=citations_from_chunks(chunks),
        )


def test_build_context_numbers_chunks_and_keeps_review_metadata():
    context = build_context(sample_retrieved_chunks())

    assert "[1]" in context
    assert "[2]" in context
    assert "Professor: Alexander Rudnick" in context
    assert "Course: CSE142" in context
    assert "Source: https://example.com/rudnick" in context
    assert "Review: Great lectures." in context


def test_build_messages_include_query_and_numbered_evidence():
    messages = build_messages(
        "What do students say about Rudnick?",
        sample_retrieved_chunks(),
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "Answer only from the provided review chunks" in messages[0]["content"]
    assert "What do students say about Rudnick?" in messages[1]["content"]
    assert "[1]" in messages[1]["content"]
    assert "Review: Helpful examples." in messages[1]["content"]


def test_citations_from_chunks_preserve_metadata():
    citations = citations_from_chunks(sample_retrieved_chunks())

    assert len(citations) == 2
    assert citations[0].index == 1
    assert citations[0].professor == "Alexander Rudnick"
    assert citations[0].course == "CSE142"
    assert citations[0].source_url == "https://example.com/rudnick"
    assert citations[0].rating_id == "111"
    assert citations[0].date == "2026-01-01"


def test_answer_question_returns_fallback_when_retrieval_has_no_chunks():
    store = FakeStore([])
    generator = FakeGenerator()

    answer = answer_question(
        "Should I take CSE143 with Alexander Rudnick?",
        store,
        sample_review_chunks(),
        generator,
    )

    assert answer.answer == (
        "I do not have matching review chunks for that professor/course "
        "in the scraped RMP data."
    )
    assert answer.citations == []
    assert generator.calls == []


def test_answer_question_calls_generator_when_chunks_exist():
    retrieved = sample_retrieved_chunks()
    store = FakeStore(retrieved)
    generator = FakeGenerator()

    answer = answer_question(
        "general Rudnick question",
        store,
        sample_review_chunks(),
        generator,
    )

    assert answer.answer == "Students say Rudnick is clear and helpful. [1]"
    assert len(answer.citations) == 2
    assert generator.calls[0]["query"] == "general Rudnick question"
    assert generator.calls[0]["chunks"] == retrieved


def test_answer_question_rejects_empty_query():
    with pytest.raises(ValueError, match="query cannot be empty"):
        answer_question("  ", FakeStore([]), sample_review_chunks(), FakeGenerator())


def test_format_answer_for_cli_prints_answer_and_sources():
    answer = GeneratedAnswer(
        answer="Students say Rudnick is helpful. [1]",
        citations=citations_from_chunks(sample_retrieved_chunks()[:1]),
    )

    output = format_answer_for_cli(answer)

    assert "Answer:\nStudents say Rudnick is helpful. [1]" in output
    assert "Sources:" in output
    assert "[1] Alexander Rudnick - CSE142 - https://example.com/rudnick" in output


def test_format_answer_for_cli_handles_no_sources():
    output = format_answer_for_cli(
        GeneratedAnswer(answer="No matching evidence.", citations=[])
    )

    assert "Answer:\nNo matching evidence." in output
    assert "Sources:\nNo sources returned." in output
