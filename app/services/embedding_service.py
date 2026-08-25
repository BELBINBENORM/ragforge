from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import settings

import logging

logger = logging.getLogger(__name__)


@lru_cache
def get_embedding_model():

    logger.info("Loading embedding model: %s", settings.embedding_model)
    return SentenceTransformer(
        settings.embedding_model
    )


def generate_embedding(
    text: str,
) -> list[float]:

    model = get_embedding_model()
    logger.debug("Generating embedding for text length=%d", len(text))

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()