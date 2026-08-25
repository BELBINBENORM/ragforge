import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import (
    ChunkModel,
    DocumentModel,
)
from app.database.session import get_db
from app.schemas.chunk import ChunkResponse
from app.schemas.document import DocumentResponse
from app.services.processing_service import (
    process_document,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path(
    settings.upload_dir
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


MAX_FILE_SIZE = (
    settings.max_file_size_mb
    * 1024
    * 1024
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
)
def upload_document(
    file: UploadFile = File(...),
    title: str = "",
    source: str = "upload",
    db: Session = Depends(get_db),
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="File name is required.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Allowed: pdf, docx, txt."
            ),
        )

    content = file.file.read()

    if not content:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail=(
                f"File exceeds the "
                f"{settings.max_file_size_mb} MB limit."
            ),
        )

    file_path = (
        UPLOAD_DIR
        / f"{uuid.uuid4()}{extension}"
    )

    try:

        file_path.write_bytes(content)

        document = DocumentModel(
            title=(
                title.strip()
                or Path(
                    file.filename
                ).stem
            ),
            source=source.strip() or "upload",
            file_path=file_path.as_posix(),
            file_type=extension.lstrip("."),
            status="uploaded",
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        return document

    except Exception:

        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise


@router.get(
    "/",
    response_model=list[DocumentResponse],
)
def get_documents(
    db: Session = Depends(get_db),
):

    return (
        db.query(DocumentModel)
        .order_by(
            DocumentModel.created_at.desc()
        )
        .all()
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):

    document = (
        db.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id
        )
        .first()
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document


@router.post(
    "/{document_id}/process",
)
def process_document_endpoint(
    document_id: int,
    db: Session = Depends(get_db),
):

    document = (
        db.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id
        )
        .first()
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    try:

        chunks = process_document(
            document,
            db,
        )

        return {
            "document_id": document.id,
            "status": document.status,
            "chunk_count": len(chunks),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {exc}",
        )


@router.get(
    "/{document_id}/chunks",
    response_model=list[ChunkResponse],
)
def get_document_chunks(
    document_id: int,
    db: Session = Depends(get_db),
):

    document = (
        db.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id
        )
        .first()
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return (
        db.query(ChunkModel)
        .filter(
            ChunkModel.document_id == document_id
        )
        .order_by(
            ChunkModel.chunk_index
        )
        .all()
    )


@router.delete(
    "/{document_id}",
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):

    document = (
        db.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id
        )
        .first()
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    file_path = Path(
        document.file_path
    )

    db.delete(document)

    db.commit()

    if file_path.exists():
        file_path.unlink()

    return {
        "message": "Document deleted.",
        "document_id": document_id,
    }