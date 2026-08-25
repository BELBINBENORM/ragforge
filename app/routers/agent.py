from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agents.agent import run_agent
from app.database.session import get_db

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


class AgentRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    session_id: int | None = Field(default=None, ge=1)


class AgentResponse(BaseModel):
    answer: str


@router.post("/", response_model=AgentResponse)
def ask_agent(
    request: AgentRequest,
    db: Session = Depends(get_db),
):
    try:
        answer = run_agent(
            db=db,
            question=request.question,
            session_id=request.session_id,
        )
        return AgentResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {exc}",
        ) from exc
