from functools import lru_cache

from app.retrieval.models import DocumentChunk, EmbeddedChunk
from sentence_transformers import SentenceTransformer
from app.core.config import settings

@lru_cache
def get_sentence_transformer():
    
    return SentenceTransformer(
        model_name_or_path=settings.embedding_model,  device=settings.embedding_device
    )

class EmbeddingGenerator:

    def __init__(self):

        self.model = get_sentence_transformer()

    def embed(self, chunks: list[DocumentChunk]) -> list[EmbeddedChunk]:

        texts = [chunk.text for chunk in chunks]

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        embedded_chunks = []
        for chunk, vector in zip(chunks, vectors):
            embedded_chunks.append(
                EmbeddedChunk(
                    chunk=chunk, embedding=vector.tolist()
                )
            )

        return embedded_chunks