from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.search import (
    SearchRequest,
    SearchResult,
)
from app.services.search_service import (
    search_similar_chunks,
)


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post(
    "/",
    response_model=list[SearchResult],
)
def search_chunks(
    request: SearchRequest,
    db: Session = Depends(get_db),
):

    results = search_similar_chunks(
        db=db,
        query=request.query,
        top_k=request.top_k,
        similarity_threshold=(
            request.similarity_threshold
        ),
    )

    return results