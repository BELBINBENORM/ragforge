from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ChatSessionCreate(BaseModel):

    title: str = Field(
        default="New Chat",
        min_length=1,
        max_length=255,
    )


class ChatSessionUpdate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255,
    )


class ChatSessionResponse(BaseModel):

    id: int

    title: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ChatMessageResponse(BaseModel):

    id: int

    session_id: int

    role: str

    content: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ChatAskRequest(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=4000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    similarity_threshold: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )


class ChatSource(BaseModel):

    id: int

    document_id: int

    document_title: str

    chunk_index: int

    content: str

    distance: float

    similarity: float


class ChatResponse(BaseModel):

    session_id: int

    question: str

    answer: str

    sources: list[ChatSource]