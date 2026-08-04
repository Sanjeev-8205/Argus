from app.retrieval.pipeline import IngestionPipeline
from pathlib import Path

def test_pipeline():

    path = Path("data/raw/hr")

    pipeline = IngestionPipeline(path)

    result = pipeline.run()

    assert result.documents_processed > 0
    assert result.chunks_created > 0
    assert result.embeddings_generated > 0