from __future__ import annotations

from dataclasses import dataclass

from training_plan_schemas.domain_v1 import TrainingSession


@dataclass(frozen=True)
class RetrievalMatch:
    session: TrainingSession
    structured_score: float
    semantic_score: float
    combined_score: float
    matched_fields: list[str]


def _tokenize(value: str) -> set[str]:
    return {token for token in value.lower().split() if token}


def _semantic_similarity(query: str, candidate: str) -> float:
    query_tokens = _tokenize(query)
    candidate_tokens = _tokenize(candidate)
    if not query_tokens or not candidate_tokens:
        return 0.0
    shared = len(query_tokens & candidate_tokens)
    union = len(query_tokens | candidate_tokens)
    if union == 0:
        return 0.0
    return shared / union


def _structured_score(query: str, session: TrainingSession) -> tuple[float, list[str]]:
    normalized = query.strip().lower()
    if not normalized:
        return 0.0, []

    fields: list[str] = []
    score = 0.0

    title = (session.title or "").lower()
    if normalized in title:
        score += 1.0
        fields.append("title")

    notes = (session.notes or "").lower()
    if normalized in notes:
        score += 0.6
        fields.append("notes")

    matching_tags = [tag for tag in session.tags if normalized in tag.lower()]
    if matching_tags:
        score += 0.5
        fields.append("tags")

    return score, fields


def _semantic_text(session: TrainingSession) -> str:
    set_labels: list[str] = []
    for block in session.blocks:
        for training_set in block.sets:
            if training_set.label:
                set_labels.append(training_set.label)

    return " ".join(
        [
            session.title or "",
            session.notes or "",
            " ".join(session.tags),
            " ".join(set_labels),
        ]
    ).strip()


def hybrid_search_sessions(
    *,
    query: str | None,
    sessions: list[TrainingSession],
    top_k: int = 20,
) -> list[RetrievalMatch]:
    if not sessions:
        return []

    normalized_query = (query or "").strip()
    if not normalized_query:
        return [
            RetrievalMatch(
                session=item,
                structured_score=0.0,
                semantic_score=0.0,
                combined_score=0.0,
                matched_fields=[],
            )
            for item in sessions[:top_k]
        ]

    matches: list[RetrievalMatch] = []
    for session in sessions:
        structured_score, matched_fields = _structured_score(normalized_query, session)
        semantic_score = _semantic_similarity(normalized_query, _semantic_text(session))
        combined_score = (structured_score * 0.65) + (semantic_score * 0.35)

        if combined_score <= 0:
            continue

        matches.append(
            RetrievalMatch(
                session=session,
                structured_score=round(structured_score, 4),
                semantic_score=round(semantic_score, 4),
                combined_score=round(combined_score, 4),
                matched_fields=matched_fields,
            )
        )

    matches.sort(key=lambda match: match.combined_score, reverse=True)
    return matches[:top_k]
