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
        self.embeddor = EmbeddingGenerator()
        self.indexer = QdrantIndexer()

        self.loader = DocumentLoader(data_directory)

    def run(self):

        documents = self.loader.load()
        print(f"Loaded {len(documents)} documents")

        embedded_chunks = []
        for document in documents:

            cleaned_document = self.cleaner.clean(document)
            enriched_document = self.extractor.extract(cleaned_document)
            document_chunks = self.chunker.chunk(enriched_document)

            embedded_document = self.embeddor.embed(document_chunks)

            embedded_chunks.extend(embedded_document)

        self.indexer.index(embedded_chunks)

        return IngestionResult(
            documents_processed=len(documents),
            chunks_created=len(embedded_chunks),
            embeddings_generated=len(embedded_chunks),
        )
