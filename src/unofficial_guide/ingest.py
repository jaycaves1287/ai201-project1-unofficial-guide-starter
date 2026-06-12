import json
import re
from html import unescape
from urllib.error import URLError
from urllib.request import Request, urlopen

from unofficial_guide.models import ProfessorSource, RatingRecord


class RelayStoreError(RuntimeError):
    """Raised when a Rate My Professors page does not expose usable review data."""


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch_html(source: ProfessorSource, timeout: int = 20) -> str:
    request = Request(source.url, headers=DEFAULT_HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except URLError as error:
        raise RelayStoreError(f"Could not fetch {source.url}: {error}") from error


def extract_relay_store(html: str) -> dict[str, object]:
    marker = "window.__RELAY_STORE__"
    marker_index = html.find(marker)
    if marker_index == -1:
        raise RelayStoreError("Could not find window.__RELAY_STORE__ in RMP HTML.")

    equals_index = html.find("=", marker_index)
    if equals_index == -1:
        raise RelayStoreError("Found __RELAY_STORE__ but could not find its value.")

    start_index = html.find("{", equals_index)
    if start_index == -1:
        raise RelayStoreError("Found __RELAY_STORE__ but JSON object was missing.")

    end_index = _find_json_object_end(html, start_index)
    raw_json = html[start_index:end_index]
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as error:
        raise RelayStoreError("Could not parse RMP relay store JSON.") from error

    if not isinstance(parsed, dict):
        raise RelayStoreError("RMP relay store was not a JSON object.")
    return parsed


def extract_ratings_from_store(store: dict[str, object]) -> list[RatingRecord]:
    ratings: list[RatingRecord] = []
    for value in store.values():
        if not isinstance(value, dict) or value.get("__typename") != "Rating":
            continue
        ratings.append(_rating_from_mapping(value))
    return ratings


def _find_json_object_end(text: str, start_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False

    for index in range(start_index, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index + 1

    raise RelayStoreError("RMP relay store JSON object was not closed.")


def _rating_from_mapping(value: dict[str, object]) -> RatingRecord:
    helpful = _to_float(value.get("helpfulRating"))
    clarity = _to_float(value.get("clarityRating"))
    return RatingRecord(
        rating_id=str(value.get("legacyId") or value.get("id") or ""),
        course=_clean_small_value(value.get("class")),
        comment=str(value.get("comment") or ""),
        date=_clean_small_value(value.get("date")),
        quality=_quality_score(helpful, clarity),
        difficulty=_to_float(value.get("difficultyRating")),
        attendance=_clean_small_value(value.get("attendanceMandatory")),
        would_take_again=_to_bool(value.get("wouldTakeAgain")),
        grade=_clean_small_value(value.get("grade")),
        textbook_use=value.get("textbookUse"),
        is_for_credit=_to_bool(value.get("isForCredit")),
        tags=_split_tags(value.get("ratingTags")),
    )


def _clean_small_value(value: object) -> str:
    return re.sub(r"\s+", " ", unescape(str(value or ""))).strip()


def _split_tags(value: object) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(
        tag
        for tag in (_clean_small_value(part) for part in str(value).split("--"))
        if tag
    )


def _to_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_bool(value: object) -> bool | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    normalized = str(value).strip().lower()
    if normalized in {"yes", "true", "1"}:
        return True
    if normalized in {"no", "false", "0"}:
        return False
    return None


def _quality_score(helpful: float | None, clarity: float | None) -> float | None:
    scores = [score for score in (helpful, clarity) if score is not None]
    if not scores:
        return None
    return round(sum(scores) / len(scores), 1)
