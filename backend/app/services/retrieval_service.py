
from app.core.config import settings
from app.retrieval.bm25 import BM25
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker


class RetrievalService:

    def __init__(self):

        self.bm25 = BM25()
        self.bm25.load(settings.bm25_index_path)

        self.hybrid_retriever = HybridRetriever(self.bm25)
        self.reranker = CrossEncoderReranker()

    def retrieve(self, query: str):

        hybrid_results = self.hybrid_retriever.retriever(
            query, 10
        )

        return self.reranker.rerank(
            query, hybrid_results, 5
        )