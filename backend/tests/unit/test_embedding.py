from pathlib import Path

from app.retrieval.embedding import EmbeddingGenerator
from app.retrieval.models import DocumentChunk, DocumentMetadata


def test_embedding():

    chunk = DocumentChunk(
        chunk_id="0",
        document_id="doc1",
        chunk_index=0,
        text = Path("data/raw/finance/budget.txt").read_text(encoding='utf-8'),
        metadata=DocumentMetadata(
            department="finance"
        )
    )

    embedding_generator = EmbeddingGenerator()

    embedding_chunk = embedding_generator.embed([chunk])

    assert embedding_chunk[0].chunk.chunk_index == 0
    assert embedding_chunk[0].chunk.chunk_id == "0"
    assert embedding_chunk[0].chunk.document_id == "doc1"
    assert embedding_chunk[0].chunk.metadata.department == "finance"
    assert len(embedding_chunk) == 1

    assert len(embedding_chunk[0].embedding) > 1