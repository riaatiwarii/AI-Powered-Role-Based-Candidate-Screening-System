"""
Configuration management for the application.
Loads settings from environment variables with sensible defaults.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App Config
    app_name: str = "AI-Powered Candidate Screening"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # Server Config
    backend_port: int = 8000
    backend_host: str = "0.0.0.0"

    # Database Config
    database_url: str = "postgresql://user:password@localhost:5432/candidate_screening"
    redis_url: str = "redis://localhost:6379/0"

    # AI/ML Config
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4-turbo"
    vector_db_type: str = "faiss"  # Options: faiss, pinecone, weaviate

    # Vector DB Config
    vector_db_dimension: int = 1536  # For OpenAI embeddings
    vector_db_path: str = "./data/vector_db"

    # RAG Config
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_retrieval: int = 5
    retrieval_threshold: float = 0.6

    # Interview Config
    max_questions_per_session: int = 5
    question_retry_count: int = 3
    session_timeout_minutes: int = 60

    # File Upload Config
    max_upload_size_mb: int = 10
    allowed_resume_formats: list = ["pdf", "txt", "docx"]
    upload_directory: str = "./uploads"

    # CORS Config
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url_async(self) -> str:
        """Convert sync database URL to async."""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")

    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
