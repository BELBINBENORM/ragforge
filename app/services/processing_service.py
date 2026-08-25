from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import ChunkModel, DocumentModel
from app.services.chunking_service import chunk_text
from app.services.document_service import extract_text
from app.services.embedding_service import generate_embedding

import logging

logger = logging.getLogger(__name__)


def process_document(
    document: DocumentModel,
    db: Session,
) -> list[ChunkModel]:

    existing_chunks = (
        db.query(ChunkModel)
        .filter(
            ChunkModel.document_id == document.id
        )
        .order_by(ChunkModel.chunk_index)
        .all()
    )

    if existing_chunks:

        document.status = "processed"

        db.commit()

        return existing_chunks

    logger.info("Processing document id=%s", document.id)
    document.status = "processing"

    db.commit()

    try:

        text = extract_text(
            file_path=document.file_path,
            file_type=document.file_type,
        )

        if not text.strip():

            raise ValueError(
                "No text could be extracted from the document."
            )

        chunks = chunk_text(
            text,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

        if not chunks:

            raise ValueError(
                "Document produced no chunks."
            )

        chunk_models = []

        for index, content in enumerate(chunks):

            embedding = generate_embedding(
                content
            )

            chunk = ChunkModel(
                document_id=document.id,
                content=content,
                chunk_index=index,
                embedding=embedding,
            )

            db.add(chunk)

            chunk_models.append(chunk)

        document.status = "processed"

        db.commit()

        for chunk in chunk_models:
            db.refresh(chunk)

        db.refresh(document)

        logger.info("Document id=%s processed with %d chunks", document.id, len(chunk_models))
        return chunk_models

    except Exception:

        logger.exception("Document processing failed for id=%s", document.id)
        db.rollback()

        document.status = "failed"

        db.commit()

        raise