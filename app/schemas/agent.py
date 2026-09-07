from pydantic import BaseModel


class AgentRequest(BaseModel):
    question: str
    session_id: int | None = None


class AgentResponse(BaseModel):
    answer: str