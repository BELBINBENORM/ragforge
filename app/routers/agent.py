from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.agents.agent import run_agent
from app.schemas.agent import AgentRequest, AgentResponse
from app.services.chat_service import save_message

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post("/run", response_model=AgentResponse)
def run_agent_endpoint(
    request: AgentRequest,
    db: Session = Depends(get_db),
):
    if request.session_id is not None:
        save_message(
            db=db,
            session_id=request.session_id,
            role="user",
            content=request.question,
        )

    answer = run_agent(
        db=db,
        question=request.question,
        session_id=request.session_id,
    )

    if request.session_id is not None:
        save_message(
            db=db,
            session_id=request.session_id,
            role="assistant",
            content=answer,
        )

    return AgentResponse(answer=answer)