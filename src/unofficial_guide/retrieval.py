import re
from dataclasses import dataclass
from typing import Iterable

from unofficial_guide.models import RetrievedChunk, ReviewChunk
from unofficial_guide.vector_store import ChromaReviewStore


@dataclass(frozen=True)
class QueryTargets:
    professors: list[str]
    courses: list[str]


@dataclass(frozen=True)
class RetrievalPlan:
    top_k: int
    where: dict[str, object] | None
    targets: QueryTargets


def retrieve(
    query: str,
    store: ChromaReviewStore,
    chunks: Iterable[ReviewChunk],
    top_k: int | None = None,
) -> list[RetrievedChunk]:
    chunk_list = list(chunks)
    plan = plan_retrieval(query, chunk_list, top_k)
    if top_k is None:
        grouped_professors = _professors_for_grouped_retrieval(plan.targets, chunk_list)
        if grouped_professors:
            results: list[RetrievedChunk] = []
            courses = plan.targets.courses if len(plan.targets.courses) == 1 else []
            for professor in grouped_professors:
                where = _where_for_targets(QueryTargets(professors=[professor], courses=courses))
                results.extend(store.query(query, top_k=3, where=where))
            return results
    return store.query(query, top_k=plan.top_k, where=plan.where)


def plan_retrieval(
    query: str,
    chunks: Iterable[ReviewChunk],
    top_k: int | None = None,
) -> RetrievalPlan:
    if not query.strip():
        raise ValueError("query cannot be empty")
    chunk_list = list(chunks)
    targets = detect_query_targets(query, chunk_list)
    if top_k is not None:
        return RetrievalPlan(top_k=top_k, where=_where_for_targets(targets), targets=targets)

    if targets.professors:
        return RetrievalPlan(
            top_k=3 * len(targets.professors),
            where=_where_for_targets(targets),
            targets=targets,
        )
    if len(targets.courses) == 1:
        professor_count = len(_professors_for_course(chunk_list, targets.courses[0]))
        return RetrievalPlan(
            top_k=min(12, max(3, 3 * professor_count)),
            where=_where_for_targets(targets),
            targets=targets,
        )
    if targets.courses:
        return RetrievalPlan(top_k=12, where=None, targets=targets)
    return RetrievalPlan(top_k=5, where=None, targets=targets)


def detect_query_targets(query: str, chunks: Iterable[ReviewChunk]) -> QueryTargets:
    normalized_query = query.lower()
    professors: list[str] = []
    for professor in _known_professors(chunks):
        pieces = professor.lower().split()
        last_name = pieces[-1] if pieces else professor.lower()
        if professor.lower() in normalized_query or last_name in normalized_query:
            professors.append(professor)

    courses = sorted(set(re.findall(r"\bCSE\s*\d+[A-Z]?\b", query, flags=re.IGNORECASE)))
    normalized_courses = [re.sub(r"\s+", "", course.upper()) for course in courses]
    return QueryTargets(professors=professors, courses=normalized_courses)


def _known_professors(chunks: Iterable[ReviewChunk]) -> list[str]:
    names = {
        str(chunk.metadata.get("professor", "")).strip()
        for chunk in chunks
        if chunk.metadata.get("professor")
    }
    return sorted(names)


def _professors_for_course(chunks: Iterable[ReviewChunk], course: str) -> list[str]:
    names = {
        str(chunk.metadata.get("professor", "")).strip()
        for chunk in chunks
        if _normalize_course(str(chunk.metadata.get("course", ""))) == course
        and chunk.metadata.get("professor")
    }
    return sorted(names)


def _professors_for_grouped_retrieval(
    targets: QueryTargets,
    chunks: Iterable[ReviewChunk],
) -> list[str]:
    if targets.professors:
        return targets.professors
    if len(targets.courses) == 1:
        return _professors_for_course(chunks, targets.courses[0])
    return []


def _where_for_targets(targets: QueryTargets) -> dict[str, object] | None:
    filters: list[dict[str, object]] = []
    if len(targets.professors) == 1:
        filters.append({"professor_normalized": targets.professors[0].strip().lower()})
    if len(targets.courses) == 1:
        filters.append({"course_normalized": targets.courses[0]})
    if len(filters) == 1:
        return filters[0]
    if len(filters) > 1:
        return {"$and": filters}
    return None


def _normalize_course(course: str) -> str:
    return re.sub(r"\s+", "", course.upper())
