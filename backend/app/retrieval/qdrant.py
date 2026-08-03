from functools import lru_cache

from app.core.config import settings
from qdrant_client import QdrantClient

@lru_cache
def get_qdrant_client() -> QdrantClient:

    return QdrantClient(
        host = settings.qdrant_host,
        port = settings.qdrant_port
    )