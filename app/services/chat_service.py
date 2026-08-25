from sqlalchemy.orm import Session

from app.config import settings
from app.database.models import (
    ChatMessage,
    ChatSession,
)


VALID_ROLES = {
    "user",
    "assistant",
}


def create_chat_session(
    db: Session,
    title: str,
) -> ChatSession:

    session = ChatSession(
        title=title.strip() or "New Chat"
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


def get_chat_session(
    db: Session,
    session_id: int,
) -> ChatSession | None:

    return (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id
        )
        .first()
    )


def get_chat_sessions(
    db: Session,
) -> list[ChatSession]:

    return (
        db.query(ChatSession)
        .order_by(
            ChatSession.created_at.desc()
        )
        .all()
    )


def get_chat_messages(
    db: Session,
    session_id: int,
    limit: int | None = None,
) -> list[ChatMessage]:

    query = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
    )

    messages = query.all()

    if limit is not None:

        messages = messages[-limit:]

    return messages


def save_message(
    db: Session,
    session_id: int,
    role: str,
    content: str,
) -> ChatMessage:

    if role not in VALID_ROLES:
        raise ValueError(
            f"Invalid message role: {role}"
        )

    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
    )

    db.add(message)

    db.commit()

    db.refresh(message)

    return message


def update_chat_title(
    db: Session,
    session: ChatSession,
    title: str,
) -> ChatSession:

    session.title = title.strip()

    db.commit()

    db.refresh(session)

    return session


def delete_chat_session(
    db: Session,
    session: ChatSession,
):

    db.delete(session)

    db.commit()