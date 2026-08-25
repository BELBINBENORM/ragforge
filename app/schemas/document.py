from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):

    id: int
    title: str
    source: str
    file_path: str
    file_type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )