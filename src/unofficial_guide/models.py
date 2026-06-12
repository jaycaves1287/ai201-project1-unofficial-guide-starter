from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProfessorSource:
    professor: str
    url: str


@dataclass(frozen=True)
class RatingRecord:
    rating_id: str
    course: str
    comment: str
    date: str
    quality: float | None
    difficulty: float | None
    attendance: str
    would_take_again: bool | None
    grade: str
    textbook_use: Any
    is_for_credit: bool | None
    tags: tuple[str, ...]


@dataclass(frozen=True)
class ReviewChunk:
    text: str
    metadata: dict[str, Any]

    def to_json(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    metadata: dict[str, Any]
    distance: float
