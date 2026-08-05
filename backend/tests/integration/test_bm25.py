from app.retrieval.pipeline import IngestionPipeline
from app.retrieval.bm25 import BM25Indexer

from pathlib import Path

def test_bm25_retriever():

    pipeline = IngestionPipeline(Path("data/raw/finance"))

    pipeline_results = pipeline.run()
    assert pipeline_results.documents_processed > 0
    assert len(pipeline_results.document_chunks) > 0

    bm25_indexer = BM25Indexer()

    bm25_indexer.build(pipeline_results.document_chunks)

    results = bm25_indexer.retrieve(
        query = "financial planning and cash flow management", top_k = 5
    )

    assert len(results) > 0
    assert results[0].score >= results[-1].score