from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Argus"
    app_version: str = "0.1.0"

    debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    embedding_model: str = "BAAI/bge-large-en-v1.5"
    embedding_device: str = "cpu"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "argus_documents"

    reranker_model: str = "BAAI/bge-reranker-base"

    data_directory: Path = Path("data/raw")

    bm25_index_path: Path = Field(default=Path("data/bm25/index.pkl"))

    gemini_api_key: str = Field(default="gemini_api_key")

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        case_sensitive=False
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()