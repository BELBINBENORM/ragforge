from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.agents.agent import run_agent
from app.schemas.agent import AgentRequest, AgentResponse


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post(
    "/run",
    response_model=AgentResponse,
)
def run_agent_endpoint(
    request: AgentRequest,
    db: Session = Depends(get_db),
):
    answer = run_agent(
        db=db,
        question=request.question,
        session_id=request.session_id,
    )

    return AgentResponse(
        answer=answer,
    )