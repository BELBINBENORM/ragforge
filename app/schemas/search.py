from pydantic import BaseModel, Field


class SearchRequest(BaseModel):

    query: str = Field(
        min_length=1,
        max_length=2000,
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


class SearchResult(BaseModel):

    id: int

    document_id: int

    document_title: str

    chunk_index: int

    content: str

    distance: float

    similarity: float