from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "Cadastre"
    app_version: str = "0.1.0"

    debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    embedding_model: str = "BAAI/bge-large-en-v1.5"
    embedding_device: str = "cpu"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "cadastre_documents"

    reranker_model: str = "BAAI/bge-reranker-base"

    data_directory: Path

    bm25_index_path: Path = Field(default=Path)

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        case_sensitive=False
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()