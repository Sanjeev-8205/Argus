from app.retrieval.bm25 import BM25Indexer
from app.retrieval.models import DocumentChunk, DocumentMetadata

def test_bm25_indexer():

    chunks = [
        DocumentChunk(
            chunk_id="1",
            document_id="doc1",
            chunk_index=0,
            text="Vacation Policy",
            metadata=DocumentMetadata(
                department="hr"
            )
        ),
        DocumentChunk(
            chunk_id="2",
            document_id="doc1",
            chunk_index=1,
            text="Company Policy",
            metadata=DocumentMetadata(
                department="hr"
            )
        ),
    ]

    indexer = BM25Indexer()
    indexer.build(chunks)

    assert indexer.index is not None
    assert len(indexer.chunks) == 2