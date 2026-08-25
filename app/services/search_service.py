from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.services.embedding_service import generate_embedding

import logging

logger = logging.getLogger(__name__)


def search_similar_chunks(
    db: Session,
    query: str,
    top_k: int | None = None,
    similarity_threshold: float | None = None,
):

    if not query.strip():
        return []

    logger.info("Vector search started")

    top_k = (
        top_k
        if top_k is not None
        else settings.top_k
    )

    similarity_threshold = (
        similarity_threshold
        if similarity_threshold is not None
        else settings.similarity_threshold
    )

    query_embedding = generate_embedding(
        query
    )

    sql = text(
        """
        SELECT
            c.id,
            c.document_id,
            d.title AS document_title,
            c.chunk_index,
            c.content,

            c.embedding <=> CAST(
                :query_embedding AS vector
            ) AS distance

        FROM chunks c

        JOIN documents d
            ON d.id = c.document_id

        WHERE c.embedding IS NOT NULL

        ORDER BY c.embedding <=> CAST(
            :query_embedding AS vector
        )

        LIMIT :top_k
        """
    )

    result = db.execute(
        sql,
        {
            "query_embedding": str(query_embedding),
            "top_k": top_k,
        },
    )

    results = []

    for row in result:

        row = dict(row._mapping)

        distance = float(
            row["distance"]
        )

        similarity = 1.0 - distance

        if similarity < similarity_threshold:
            continue

        row["distance"] = distance
        row["similarity"] = similarity

        results.append(row)

    logger.info("Vector search completed: %d results", len(results))
    return results