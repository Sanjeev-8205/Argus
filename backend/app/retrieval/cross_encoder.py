from functools import lru_cache

from sentence_transformers import CrossEncoder
from app.core.config import settings

@lru_cache
def get_cross_encoder():

    return CrossEncoder(
        model_name_or_path=settings.reranker_model,
        device=settings.embedding_device
    )