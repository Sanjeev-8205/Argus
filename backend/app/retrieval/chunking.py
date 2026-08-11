from app.retrieval.models import DocumentChunk, EnrichedDocument
from app.retrieval.tokenizer import get_tokenizer


class FixedSizeChunker:

    def __init__(self, chunk_size=512, overlap=64):

        if overlap >= chunk_size:
            raise ValueError(
                "Overlap must be smaller than chunk size."
            )
        
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.tokenizer = get_tokenizer()

    def chunk(self, document: EnrichedDocument) -> list[DocumentChunk]:

        token_ids = self.tokenizer.encode(
            document.text, add_special_tokens=False
        )

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(token_ids):

            end = start + self.chunk_size

            chunk_tokens = token_ids[start: end]

            chunk_text = self.tokenizer.decode(
                chunk_tokens, skip_special_tokens = True
            )

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