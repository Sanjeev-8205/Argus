from app.retrieval.models import (
    EnrichedDocument, DocumentChunk
)

class FixedSizeChunker:

    def __init__(self, chunk_size=500, overlap=50):

        if overlap >= chunk_size:
            raise ValueError(
                "Overlap must be smaller than chunk size."
            )
        
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document: EnrichedDocument) -> list[DocumentChunk]:

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(document.text):

            end = start + self.chunk_size

            chunk_text = document.text[start: end]

            chunks.append(
                DocumentChunk(
                    chunk_id=f"{document.document_id}_{chunk_index}",
                    document_id=document.document_id,
                    chunk_index=chunk_index,
                    text=chunk_text,
                    metadata=document.metadata
                )
            )

            start += self.chunk_size - self.overlap

            chunk_index += 1

        return chunks