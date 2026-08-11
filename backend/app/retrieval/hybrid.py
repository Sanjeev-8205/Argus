from app.retrieval.bm25 import BM25
from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import DenseRetriever


class HybridRetriever:

    RRF_K = 60

    def __init__(self, bm25: BM25):

        self.dense = DenseRetriever()
        self.bm25 = bm25

    def retriever(self, query: str, top_k: int = 5) -> list[RetrievalResult]:

        dense_results = self.dense.retrieve(
            query, top_k
        )

        bm25_results = self.bm25.retrieve(
            query, top_k
        )

        return self._rrf(
            dense_results,
            bm25_results,
            top_k
        )

    def _rrf(
        self, 
        dense_results: list[RetrievalResult], 
        bm25_results: list[RetrievalResult],
        top_k: int
    ) -> list[RetrievalResult]:

        rrf_scores = {}
        chunk_lookup = {}

        for rank, result in enumerate(dense_results, start=1):

            chunk_id = result.chunk.chunk_id

            chunk_lookup[chunk_id] = result.chunk

            rrf_scores.setdefault(chunk_id, 0.0)

            rrf_scores[chunk_id] += (
                1/(self.RRF_K+rank)
            )

        for rank, result in enumerate(bm25_results, start=1):

            chunk_id = result.chunk.chunk_id

            chunk_lookup[chunk_id] = result.chunk

            rrf_scores.setdefault(chunk_id, 0.0)

            rrf_scores[chunk_id] += (
                1/(self.RRF_K+rank)
            )

        sorted_chunks = sorted(
            rrf_scores.items(), key=lambda x:x[1], reverse=True
        )

        results = []

        for chunk_id, score in sorted_chunks[:top_k]:

            results.append(
                RetrievalResult(
                    chunk=chunk_lookup[chunk_id],
                    score=score
                )
            )

        return results