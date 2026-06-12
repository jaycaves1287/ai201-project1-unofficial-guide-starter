import json
from pathlib import Path

import pytest

from unofficial_guide.models import ReviewChunk
from unofficial_guide.retrieval import detect_query_targets, plan_retrieval, retrieve
from unofficial_guide.vector_store import (
    ChromaReviewStore,
    load_chunks_jsonl,
    make_chunk_id,
    normalize_metadata,
)


class FakeEmbedder:
    def embed_texts(self, texts):
        return [_embedding_for(text) for text in texts]

    def embed_query(self, query):
        return _embedding_for(query)


def _embedding_for(text):
    lower = text.lower()
    if "rudnick" in lower:
        return [1.0, 0.0, 0.0]
    if "flanagan" in lower:
        return [0.0, 1.0, 0.0]
    return [0.0, 0.0, 1.0]


def sample_chunks():
    return [
        ReviewChunk(
            text="Professor: Alexander Rudnick\nCourse: CSE142\nReview: Great lectures.",
            metadata={
                "source_type": "rmp",
                "source_url": "https://example.com/rudnick",
                "professor": "Alexander Rudnick",
                "course": "CSE142",
                "rating_id": "111",
                "date": "2026-01-01",
                "quality": 5.0,
                "difficulty": 2.0,
                "chunk_index": 0,
                "chunk_part": 0,
            },
        ),
        ReviewChunk(
            text="Professor: Cormac Flanagan\nCourse: CSE114A\nReview: Helpful old exams.",
            metadata={
                "source_type": "rmp",
                "source_url": "https://example.com/flanagan",
                "professor": "Cormac Flanagan",
                "course": "CSE114A",
                "rating_id": "222",
                "date": "2025-03-31",
                "quality": 5.0,
                "difficulty": 3.0,
                "chunk_index": 1,
                "chunk_part": 0,
            },
        ),
    ]


def course_comparison_chunks():
    return sample_chunks() + [
        ReviewChunk(
            text="Professor: Cormac Flanagan\nCourse: CSE142\nReview: Clear examples.",
            metadata={
                "source_type": "rmp",
                "source_url": "https://example.com/flanagan-cse142",
                "professor": "Cormac Flanagan",
                "course": "CSE142",
                "rating_id": "333",
                "date": "2025-04-01",
                "quality": 4.0,
                "difficulty": 3.0,
                "chunk_index": 2,
                "chunk_part": 0,
            },
        )
    ]


def test_load_chunks_jsonl_reads_valid_review_chunks():
    path = Path("tests") / "_sample_chunks.jsonl"
    payload = [chunk.to_json() for chunk in sample_chunks()]
    try:
        path.write_text(
            "\n".join(json.dumps(item) for item in payload) + "\n",
            encoding="utf-8",
        )

        chunks = load_chunks_jsonl(path)

        assert len(chunks) == 2
        assert chunks[0].metadata["professor"] == "Alexander Rudnick"
        assert chunks[1].text.startswith("Professor: Cormac Flanagan")
    finally:
        path.unlink(missing_ok=True)


def test_load_chunks_jsonl_rejects_missing_required_metadata():
    path = Path("tests") / "_bad_chunks.jsonl"
    try:
        path.write_text(
            json.dumps({"text": "Missing course", "metadata": {"professor": "A"}}),
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="course"):
            load_chunks_jsonl(path)
    finally:
        path.unlink(missing_ok=True)


def test_make_chunk_id_is_stable_and_filename_safe():
    chunk = sample_chunks()[0]

    assert make_chunk_id(chunk) == "alexander-rudnick-cse142-111-0"


def test_normalize_metadata_keeps_only_chroma_safe_values():
    normalized = normalize_metadata(
        {
            "professor": "Alexander Rudnick",
            "course": "CSE 142",
            "quality": 5.0,
            "chunk_index": 0,
            "would_take_again": True,
            "missing": None,
            "tags": ["Great"],
        }
    )

    assert normalized == {
        "professor": "Alexander Rudnick",
        "course": "CSE 142",
        "quality": 5.0,
        "chunk_index": 0,
        "would_take_again": True,
        "missing": "",
        "tags": "['Great']",
        "professor_normalized": "alexander rudnick",
        "course_normalized": "CSE142",
    }


@pytest.mark.parametrize(
    ("query", "professors", "courses"),
    [
        ("What do students say about Rudnick?", ["Alexander Rudnick"], []),
        ("Is CSE114A hard with Flanagan?", ["Cormac Flanagan"], ["CSE114A"]),
        ("What about CSE 142 workload?", [], ["CSE142"]),
    ],
)
def test_detect_query_targets_finds_professors_and_courses(query, professors, courses):
    targets = detect_query_targets(query, sample_chunks())

    assert targets.professors == professors
    assert targets.courses == courses


def test_plan_retrieval_uses_dynamic_top_k_rules():
    chunks = course_comparison_chunks()

    general_plan = plan_retrieval("general workload question", chunks)
    professor_plan = plan_retrieval("Rudnick lectures", chunks)
    course_plan = plan_retrieval("Best professor for CSE114A", chunks)
    professor_course_plan = plan_retrieval("Is CSE114A hard with Flanagan?", chunks)
    comparison_plan = plan_retrieval("Best professor for CSE142", chunks)

    assert general_plan.top_k == 5
    assert general_plan.where is None
    assert professor_plan.top_k == 3
    assert professor_plan.where == {"professor_normalized": "alexander rudnick"}
    assert course_plan.top_k == 3
    assert course_plan.where == {"course_normalized": "CSE114A"}
    assert professor_course_plan.top_k == 3
    assert professor_course_plan.where == {
        "$and": [
            {"professor_normalized": "cormac flanagan"},
            {"course_normalized": "CSE114A"},
        ]
    }
    assert comparison_plan.top_k == 6


def test_chroma_store_rebuilds_and_queries_with_fake_embeddings():
    chunks = sample_chunks()
    store = ChromaReviewStore.in_memory("test_reviews", FakeEmbedder())

    store.rebuild(chunks)
    first_count = store.count()
    store.rebuild(chunks)
    second_count = store.count()
    results = store.query("Rudnick lectures", top_k=1)
    filtered_results = store.query(
        "lectures",
        top_k=2,
        where={"course_normalized": "CSE142"},
    )

    assert first_count == 2
    assert second_count == 2
    assert len(results) == 1
    assert results[0].metadata["professor"] == "Alexander Rudnick"
    assert isinstance(results[0].distance, float)
    assert len(filtered_results) == 1
    assert filtered_results[0].metadata["course_normalized"] == "CSE142"


def test_retrieve_gets_reviews_for_each_professor_in_a_course():
    chunks = course_comparison_chunks()
    store = ChromaReviewStore.in_memory("test_course_reviews", FakeEmbedder())

    store.rebuild(chunks)
    results = retrieve("Best professor for CSE142", store, chunks)

    assert len(results) == 2
    assert {result.metadata["professor"] for result in results} == {
        "Alexander Rudnick",
        "Cormac Flanagan",
    }
    assert {result.metadata["course_normalized"] for result in results} == {"CSE142"}
