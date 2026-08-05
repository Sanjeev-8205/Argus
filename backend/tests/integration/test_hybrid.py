from pathlib import Path

from app.retrieval.bm25 import BM25
from app.retrieval.hybrid import HybridRetriever
from app.core.config import settings

def test_hybrid_retriever():

    bm25 = BM25()
    bm25.load(settings.bm25_index_path)

    hybrid_retriever = HybridRetriever(bm25)

    results = hybrid_retriever.retriever(
        "company policy leave benefits", 3
    )

    assert len(results) > 0
    assert len(results) == 3
    assert results[0].score>0
    assert results[0].score >= results[-1].score
