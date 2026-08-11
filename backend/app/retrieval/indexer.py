from uuid import NAMESPACE_DNS, uuid5

from qdrant_client import models
from qdrant_client.models import PointStruct

from app.core.config import settings
from app.retrieval.models import EmbeddedChunk
from app.retrieval.qdrant import get_qdrant_client


class QdrantIndexer:
    
    def __init__(self):

        self.client = get_qdrant_client()

        self.collection_name = settings.qdrant_collection

    def create_collection(
            self, vector_size: int,
    ):

        collections = self.client.get_collections()

        existing = {
            c.name
            for c in collections.collections
        }

        if self.collection_name in existing:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            )
        )

    def index(self, chunks: list[EmbeddedChunk]):
        if not chunks:
            return

        self.create_collection(
            len(chunks[0].embedding)
        )

        points = []

        for chunk in chunks:

            points.append(
                PointStruct(
                    id = str(uuid5(NAMESPACE_DNS, chunk.chunk.chunk_id)),
                    vector = chunk.embedding,

                    payload = {
                        "document_id": chunk.chunk.document_id,
                        "chunk_id": chunk.chunk.chunk_id,
                        "chunk_index": chunk.chunk.chunk_index,
                        "text": chunk.chunk.text,
                        "department": chunk.chunk.metadata.department
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )