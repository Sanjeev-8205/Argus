from app.retrieval.cross_encoder import get_cross_encoder
from app.retrieval.models import RetrievalResult


class CrossEncoderReranker:

    def __init__(self):

        self.model = get_cross_encoder()

    def rerank(
        self, 
        query: str, 
        candidates: list[RetrievalResult], 
        top_k: int = 5
    ) -> list[RetrievalResult]:

        pairs = [
            (query, c.chunk.text)
            for c in candidates
        ]

        scores = self.model.predict(pairs)

        reranked = []
        for candidate, score in zip(candidates, scores):

            reranked.append(
                RetrievalResult(
                    chunk=candidate.chunk,
                    score=float(score)
                )
            )

        reranked.sort(
            key=lambda x:x.score, reverse=True
        )

        return reranked[:top_k]