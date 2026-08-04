from app.retrieval.ingest import DocumentLoader
from app.retrieval.cleaning import TextCleaner
from app.retrieval.metadata import MetadataExtractor
from app.retrieval.chunking import FixedSizeChunker
from app.retrieval.embedding import EmbeddingGenerator
from app.retrieval.indexer import QdrantIndexer

from app.retrieval.models import IngestionResult

from pathlib import Path

class IngestionPipeline:

    def __init__(self, data_directory: Path):

        self.cleaner = TextCleaner()
        self.extractor = MetadataExtractor()
        self.chunker = FixedSizeChunker()
        self.embedder = EmbeddingGenerator()
        self.indexer = QdrantIndexer()

        self.docs = DocumentLoader(data_directory).load()

    def run(self):

        print(f"Loaded {len(self.docs)} documents")

        document_chunks = []
        embedded_chunks = []
        for document in self.docs:

            cleaned_document = self.cleaner.clean(document)
            enriched_document = self.extractor.extract(cleaned_document)
            doc_chunks = self.chunker.chunk(enriched_document)
            document_chunks.extend(doc_chunks)

            embedded_document = self.embedder.embed(doc_chunks)

            embedded_chunks.extend(embedded_document)

        self.indexer.index(embedded_chunks)

        return IngestionResult(
            documents_processed=len(self.docs),
            chunks_created=len(document_chunks),
            embeddings_generated=len(embedded_chunks),
            document_chunks=document_chunks
        )
