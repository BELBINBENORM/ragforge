from sqlalchemy.orm import Session

from app.services.search_service import search_similar_chunks
from app.services.chat_service import get_chat_messages


def search_documents(
    db: Session,
    query: str,
    top_k: int = 5,
):
    results = search_similar_chunks(
        db=db,
        query=query,
        top_k=top_k,
    )
    return [
        {
            "document_id": r["document_id"],
            "document_title": r["document_title"],
            "chunk_index": r["chunk_index"],
            "content": r["content"],
            "similarity": r["similarity"],
        }
        for r in results
    ]


def get_conversation_history(
    db: Session,
    session_id: int,
    limit: int = 10,
):
    messages = get_chat_messages(
        db=db,
        session_id=session_id,
        limit=limit,
    )
    return [
        {"role": message.role, "content": message.content}
        for message in messages
    ]
