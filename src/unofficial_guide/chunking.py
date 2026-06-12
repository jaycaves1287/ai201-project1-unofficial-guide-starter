import re
from html import unescape
from typing import Iterable

from unofficial_guide.models import ProfessorSource, RatingRecord, ReviewChunk


def clean_text(text: str) -> str:
    decoded = unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", decoded).strip()


def chunk_ratings(
    source: ProfessorSource,
    ratings: Iterable[RatingRecord],
    max_tokens: int = 400,
    overlap_tokens: int = 60,
) -> list[ReviewChunk]:
    chunks: list[ReviewChunk] = []
    for rating in ratings:
        cleaned_comment = clean_text(rating.comment)
        if not cleaned_comment:
            continue

        comment_parts = split_long_text(cleaned_comment, max_tokens, overlap_tokens)
        for part_index, comment_part in enumerate(comment_parts):
            metadata = _metadata_for_rating(source, rating, len(chunks), part_index)
            chunks.append(
                ReviewChunk(
                    text=_format_chunk_text(source, rating, comment_part),
                    metadata=metadata,
                )
            )
    return chunks


def split_long_text(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return [text]
    if overlap_tokens >= max_tokens:
        raise ValueError("overlap_tokens must be smaller than max_tokens")

    parts: list[str] = []
    step = max_tokens - overlap_tokens
    for start in range(0, len(tokens), step):
        window = tokens[start : start + max_tokens]
        if window:
            parts.append(" ".join(window))
        if start + max_tokens >= len(tokens):
            break
    return parts


def _format_chunk_text(
    source: ProfessorSource,
    rating: RatingRecord,
    comment: str,
) -> str:
    lines = [
        f"Professor: {source.professor}",
        f"Course: {_display(rating.course)}",
        f"Date: {_display(rating.date)}",
        f"Quality: {_display(rating.quality)}",
        f"Difficulty: {_display(rating.difficulty)}",
        f"Attendance: {_display(rating.attendance)}",
        f"Would Take Again: {_display_bool(rating.would_take_again)}",
        f"Grade: {_display(rating.grade)}",
        f"Tags: {_display(', '.join(rating.tags))}",
        f"Review: {comment}",
    ]
    return "\n".join(lines)


def _metadata_for_rating(
    source: ProfessorSource,
    rating: RatingRecord,
    chunk_index: int,
    part_index: int,
) -> dict[str, object]:
    return {
        "source_type": "rmp",
        "source_url": source.url,
        "professor": source.professor,
        "course": rating.course,
        "rating_id": rating.rating_id,
        "date": rating.date,
        "quality": rating.quality,
        "difficulty": rating.difficulty,
        "chunk_index": chunk_index,
        "chunk_part": part_index,
    }


def _display(value: object) -> str:
    if value is None or value == "":
        return "N/A"
    return str(value)


def _display_bool(value: bool | None) -> str:
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return "N/A"
