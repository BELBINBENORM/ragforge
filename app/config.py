from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str

    llm_provider: str = "gemini"
    gemini_api_key: str
    gemini_model: str = "gemini-3.6-flash"

    embedding_model: str = "all-MiniLM-L6-v2"

    upload_dir: str = "data/documents"

    chunk_size: int = 1000
    chunk_overlap: int = 200

    top_k: int = 5
    similarity_threshold: float = 0.35

    max_file_size_mb: int = 20

    max_chat_history: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()