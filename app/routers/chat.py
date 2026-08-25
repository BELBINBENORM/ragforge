from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db

from app.schemas.chat import (
    ChatAskRequest,
    ChatMessageResponse,
    ChatResponse,
    ChatSessionCreate,
    ChatSessionResponse,
    ChatSessionUpdate,
)

from app.services.chat_service import (
    create_chat_session,
    delete_chat_session,
    get_chat_messages,
    get_chat_session,
    get_chat_sessions,
    save_message,
    update_chat_title,
)

from app.services.llm_service import (
    generate_answer,
)

from app.services.search_service import (
    search_similar_chunks,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/sessions",
    response_model=ChatSessionResponse,
)
def create_session(
    request: ChatSessionCreate,
    db: Session = Depends(get_db),
):

    return create_chat_session(
        db=db,
        title=request.title,
    )


@router.get(
    "/sessions",
    response_model=list[ChatSessionResponse],
)
def list_sessions(
    db: Session = Depends(get_db),
):

    return get_chat_sessions(
        db
    )


@router.get(
    "/sessions/{session_id}",
    response_model=ChatSessionResponse,
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
):

    session = get_chat_session(
        db=db,
        session_id=session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    return session


@router.patch(
    "/sessions/{session_id}",
    response_model=ChatSessionResponse,
)
def update_session(
    session_id: int,
    request: ChatSessionUpdate,
    db: Session = Depends(get_db),
):

    session = get_chat_session(
        db=db,
        session_id=session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    return update_chat_title(
        db=db,
        session=session,
        title=request.title,
    )


@router.delete(
    "/sessions/{session_id}",
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
):

    session = get_chat_session(
        db=db,
        session_id=session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    delete_chat_session(
        db=db,
        session=session,
    )

    return {
        "message": "Chat session deleted.",
        "session_id": session_id,
    }


@router.get(
    "/sessions/{session_id}/messages",
    response_model=list[ChatMessageResponse],
)
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
):

    session = get_chat_session(
        db=db,
        session_id=session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    return get_chat_messages(
        db=db,
        session_id=session_id,
    )


@router.post(
    "/sessions/{session_id}/ask",
    response_model=ChatResponse,
)
def ask_question(
    session_id: int,
    request: ChatAskRequest,
    db: Session = Depends(get_db),
):

    session = get_chat_session(
        db=db,
        session_id=session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    previous_messages = get_chat_messages(
        db=db,
        session_id=session_id,
        limit=settings.max_chat_history,
    )

    chat_history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in previous_messages
    ]

    results = search_similar_chunks(
        db=db,
        query=request.question,
        top_k=request.top_k,
        similarity_threshold=(
            request.similarity_threshold
        ),
    )

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
Source document: {result["document_title"]}
Document ID: {result["document_id"]}
Chunk index: {result["chunk_index"]}
Similarity: {result["similarity"]:.4f}

{result["content"]}
"""
        )

    if context_parts:

        context = "\n\n---\n\n".join(
            context_parts
        )

    else:

        context = (
            "No relevant document context "
            "was retrieved."
        )

    save_message(
        db=db,
        session_id=session_id,
        role="user",
        content=request.question,
    )

    try:

        answer = generate_answer(
            question=request.question,
            context=context,
            chat_history=chat_history,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"LLM service unavailable: {exc}",
        )

    save_message(
        db=db,
        session_id=session_id,
        role="assistant",
        content=answer,
    )

    return {
        "session_id": session_id,
        "question": request.question,
        "answer": answer,
        "sources": results,
    }