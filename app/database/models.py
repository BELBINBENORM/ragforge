from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DocumentModel(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="upload" )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False )
    file_type: Mapped[str] = mapped_column(String(50), nullable=False )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="uploaded" )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False )
    chunks: Mapped[list["ChunkModel"]] = relationship(back_populates="document", cascade="all, delete-orphan" )


class ChunkModel(Base):

    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True )
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id",ondelete="CASCADE"),nullable=False,index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(384),nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,nullable=False)
    document: Mapped["DocumentModel"] = relationship(back_populates="chunks")


class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(255),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id",ondelete="CASCADE"),nullable=False,index=True)
    role: Mapped[str] = mapped_column(String(20),nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,nullable=False)
    session: Mapped["ChatSession"] = relationship(back_populates="messages")