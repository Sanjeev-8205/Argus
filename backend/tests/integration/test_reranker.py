from app.retrieval.reranker import Reranker
from app.retrieval.pipeline import IngestionPipeline
from app.retrieval.hybrid import HybridRetriever

from pathlib import Path

def test_reranker():

    pipeline = IngestionPipeline(Path("data/raw/hr"))
    ingestion_result = pipeline.run()

    query = "employee leave attendance benefits compensation conduct policy"

    hybrid_retriever = HybridRetriever(ingestion_result.document_chunks)

    hybrid_results = hybrid_retriever.retriever(
        query, 10
    )

    reranker = Reranker()
    
    reranker_results = reranker.rerank(
        query, hybrid_results, 5
    )

    assert len(reranker_results) > 0
    assert len(reranker_results) == 5
    assert reranker_results[0].score !=0
    assert reranker_results[0].score >= reranker_results[-1].score