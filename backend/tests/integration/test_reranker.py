from app.core.config import settings
from app.retrieval.bm25 import BM25
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker


def test_reranker():

    bm25 = BM25()
    bm25.load(settings.bm25_index_path)

    query = "employee leave attendance benefits compensation conduct policy"

    hybrid_retriever = HybridRetriever(bm25)

    hybrid_results = hybrid_retriever.retriever(
        query, 10
    )

    reranker = CrossEncoderReranker()
    
    reranker_results = reranker.rerank(
        query, hybrid_results, 5
    )

    assert len(reranker_results) > 0
    assert len(reranker_results) == 5
    assert reranker_results[0].score !=0
    assert reranker_results[0].score >= reranker_results[-1].score