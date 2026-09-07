from fastapi import APIRouter
from sqlalchemy import text

from app.config import settings
from app.database.connection import engine
from google import genai


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health():
    return {
        "status": "ok",
        "service": "RAGForge API",
    }


@router.get("/database")
def database_health():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT 1")
            )
            result.scalar()

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception as exc:
        return {
            "status": "error",
            "database": str(exc),
        }


@router.get("/llm")
def llm_health():
    try:
        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        response = client.models.get(
            model=settings.gemini_model
        )

        return {
            "status": "ok",
            "provider": "Google Gemini",
            "model": response.name,
            "available": True,
        }

    except Exception as exc:
        return {
            "status": "error",
            "provider": "Google Gemini",
            "model": settings.gemini_model,
            "available": False,
            "llm": str(exc),
        }
