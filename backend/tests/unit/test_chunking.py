from pathlib import Path

from app.retrieval.models import EnrichedDocument, DocumentMetadata
from app.retrieval.chunking import FixedSizeChunker

def test_chunking():

    chunker = FixedSizeChunker()

    file_path = Path("data/raw/hr/company_policy.txt")
    enriched_document = EnrichedDocument(
        document_id="doc1",
        source_path=file_path,
        text=file_path.read_text(encoding='utf-8'),
        metadata=DocumentMetadata(
            department="hr"
        )
    )

    chunked_document = chunker.chunk(enriched_document)

    assert len(chunked_document) == 32
    assert chunked_document[0].chunk_index == 0
    assert chunked_document[1].chunk_index == 1
    assert chunked_document[2].chunk_index == 2
    assert chunked_document[3].chunk_index == 3
    assert chunked_document[4].chunk_index == 4

    assert chunked_document[0].metadata.department == 'hr'