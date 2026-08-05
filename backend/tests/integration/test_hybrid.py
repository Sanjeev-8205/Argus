from pathlib import Path

from app.retrieval.hybrid import HybridRetriever
from app.retrieval.pipeline import IngestionPipeline

def test_hybrid_retriever():

    pipeline = IngestionPipeline(Path("data/raw/finance"))

    ingestion_result = pipeline.run()

    hybrid_retriever = HybridRetriever(ingestion_result.document_chunks)

    results = hybrid_retriever.retriever(
        "company policy leave benefits", 3
    )

    assert len(results) > 0
    assert len(results) == 3
    assert results[0].score>0
    assert results[0].score >= results[-1].score
