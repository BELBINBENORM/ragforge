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