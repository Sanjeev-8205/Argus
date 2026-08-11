from app.core.config import settings
from app.retrieval.embedding import get_sentence_transformer
from app.retrieval.models import DocumentChunk, DocumentMetadata, RetrievalResult
from app.retrieval.qdrant import get_qdrant_client


class DenseRetriever:

    def __init__(self):

        self.client = get_qdrant_client()
        self.collection_name = settings.qdrant_collection
        self.model = get_sentence_transformer()

    def _embed_query(
        self, query: str
    ) -> list[float]:
        
        vectors = self.model.encode(
            query,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return vectors.tolist()

    def retrieve(
        self, query: str, topk: int = 5
    ):
        query_vector = self._embed_query(query)

        search_results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=topk
        )

        results = []

        for point in search_results.points:

            payload = point.payload

            chunk = DocumentChunk(
                chunk_id=payload["chunk_id"],
                document_id=payload["document_id"],
                chunk_index=payload["chunk_index"],
                text=payload["text"],
                metadata=DocumentMetadata(
                    department=payload["department"]
                )
            )

            results.append(
                RetrievalResult(
                    chunk=chunk,
                    score=point.score
                )
            )

        return results