from fastapi import APIRouter
from sqlalchemy import text

import ollama

from app.config import settings
from app.database.connection import engine


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health():
    return {
        "status": "ok",
        "service": "AI Knowledge Platform",
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
        response = ollama.list()

        models = []

        for model in response.models:
            models.append(model.model)

        available = any(
            model.split(":")[0] == settings.ollama_model
            or model == settings.ollama_model
            for model in models
        )

        return {
            "status": "ok" if available else "warning",
            "model": settings.ollama_model,
            "available": available,
            "installed_models": models,
        }

    except Exception as exc:
        return {
            "status": "error",
            "llm": str(exc),
        }