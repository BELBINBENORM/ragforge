from pydantic import BaseModel, ConfigDict


class ChunkResponse(BaseModel):

    id: int
    document_id: int
    chunk_index: int
    content: str

    model_config = ConfigDict(
        from_attributes=True
    )