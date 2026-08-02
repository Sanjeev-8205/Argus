from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Cadastre"
    app_version: str = "0.1.0"

    debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    embedding_model: str = "BAAI/bge-large-en-v1.5"

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        case_sensitive=False
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()