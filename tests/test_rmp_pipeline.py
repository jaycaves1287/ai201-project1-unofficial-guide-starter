import json
from pathlib import Path

import pytest

from unofficial_guide.chunking import chunk_ratings, clean_text
from unofficial_guide.ingest import RelayStoreError, extract_ratings_from_store, extract_relay_store
from unofficial_guide.models import ProfessorSource
from unofficial_guide.pipeline import build_chunks_from_html, write_chunks_jsonl


SAMPLE_HTML = """
<html>
<head><title>Sample RMP Page</title></head>
<body>
<script>
window.__RELAY_STORE__ = {
  "teacher-1": {
    "__typename": "Teacher",
    "firstName": "Alexander",
    "lastName": "Rudnick",
    "legacyId": 2762323
  },
  "rating-1": {
    "__typename": "Rating",
    "comment": "Great&nbsp;professor. He&#x27;s helpful.  ",
    "legacyId": 111,
    "date": "2026-01-02 00:00:00 +0000 UTC",
    "class": "CSE143",
    "helpfulRating": 5,
    "clarityRating": 4,
    "difficultyRating": 2,
    "attendanceMandatory": "mandatory",
    "wouldTakeAgain": 1,
    "grade": "A",
    "textbookUse": -1,
    "isForCredit": true,
    "ratingTags": "Amazing lectures --Caring"
  },
  "rating-2": {
    "__typename": "Rating",
    "comment": "   ",
    "legacyId": 112,
    "date": "2026-01-03 00:00:00 +0000 UTC",
    "class": "CSE142",
    "helpfulRating": 3,
    "clarityRating": 3,
    "difficultyRating": 4,
    "attendanceMandatory": "non mandatory",
    "wouldTakeAgain": 0,
    "grade": "",
    "textbookUse": null,
    "isForCredit": true,
    "ratingTags": ""
  },
  "course-1": {
    "__typename": "Course",
    "courseName": "CSE143"
  }
};
</script>
</body>
</html>
"""


def test_extract_relay_store_reads_embedded_rmp_json():
    store = extract_relay_store(SAMPLE_HTML)

    assert store["teacher-1"]["firstName"] == "Alexander"
    assert store["rating-1"]["comment"].startswith("Great&nbsp;professor")


def test_extract_relay_store_fails_clearly_when_missing():
    with pytest.raises(RelayStoreError, match="__RELAY_STORE__"):
        extract_relay_store("<html>No relay store here</html>")


def test_extract_ratings_from_store_only_returns_rating_records():
    ratings = extract_ratings_from_store(extract_relay_store(SAMPLE_HTML))

    assert [rating.rating_id for rating in ratings] == ["111", "112"]
    assert ratings[0].course == "CSE143"
    assert ratings[0].quality == 4.5
    assert ratings[0].difficulty == 2.0


def test_clean_text_decodes_entities_and_collapses_whitespace():
    assert clean_text("Great&nbsp;professor. He&#x27;s   helpful.\n\n") == (
        "Great professor. He's helpful."
    )


def test_chunk_ratings_keeps_one_non_empty_review_per_chunk_with_metadata():
    source = ProfessorSource(
        professor="Alexander Rudnick",
        url="https://www.ratemyprofessors.com/professor/2762323",
    )
    ratings = extract_ratings_from_store(extract_relay_store(SAMPLE_HTML))

    chunks = chunk_ratings(source, ratings)

    assert len(chunks) == 1
    chunk = chunks[0]
    assert "Professor: Alexander Rudnick" in chunk.text
    assert "Course: CSE143" in chunk.text
    assert "Review: Great professor. He's helpful." in chunk.text
    assert chunk.metadata["source_type"] == "rmp"
    assert chunk.metadata["source_url"] == source.url
    assert chunk.metadata["professor"] == "Alexander Rudnick"
    assert chunk.metadata["course"] == "CSE143"
    assert chunk.metadata["rating_id"] == "111"
    assert chunk.metadata["quality"] == 4.5
    assert chunk.metadata["difficulty"] == 2.0
    assert chunk.metadata["chunk_index"] == 0


def test_pipeline_builds_chunks_from_html_and_writes_jsonl():
    source = ProfessorSource(
        professor="Alexander Rudnick",
        url="https://www.ratemyprofessors.com/professor/2762323",
    )
    output_path = Path("tests") / "_chunks_test_output.jsonl"

    try:
        chunks = build_chunks_from_html(source, SAMPLE_HTML)
        write_chunks_jsonl(chunks, output_path)

        lines = output_path.read_text(encoding="utf-8").splitlines()
        payload = json.loads(lines[0])
        assert len(chunks) == 1
        assert len(lines) == 1
        assert payload["text"] == chunks[0].text
        assert payload["metadata"]["professor"] == "Alexander Rudnick"
    finally:
        output_path.unlink(missing_ok=True)
