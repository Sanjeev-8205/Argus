from app.core.config import settings
from app.retrieval.bm25 import BM25
from app.retrieval.pipeline import IngestionPipeline

pipeline = IngestionPipeline(settings.data_directory)
ingestion_results = pipeline.run()

bm25 = BM25()

bm25.build(ingestion_results.document_chunks)
bm25.save(settings.bm25_index_path)

print("Indexes built successfully.")