from functools import lru_cache

from transformers import AutoTokenizer

from app.core.config import settings


@lru_cache
def get_tokenizer():

    return AutoTokenizer.from_pretrained(
        settings.embedding_model
    )