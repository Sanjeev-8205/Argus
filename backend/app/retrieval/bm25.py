import pickle
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

from app.retrieval.models import DocumentChunk, RetrievalResult


class BM25:

    def __init__(self):

        self.index = None
        self.chunks = []

    def build(self, chunks: list[DocumentChunk]):

        corpus = [
            chunk.text.lower().split()
            for chunk in chunks
        ]

        self.index = BM25Okapi(corpus)
        self.chunks = chunks

        print(f"Corpus:\n{corpus}\n\nIndex:\n{self.index}\n\nChunks:\n{self.chunks}")

    def retrieve(
                    self, query: str, top_k: int = 5
            ):
        
            if self.index is None:
                raise RuntimeError(
                    "BM25 index has not been built."
                )
    
            query_tokens = query.lower().split()
    
            scores = self.index.get_scores(query_tokens)
    
            top_indices = np.argsort(scores)[::-1][:top_k]
    
            results = []
    
            for idx in top_indices:
                results.append(
                    RetrievalResult(
                        chunk=self.chunks[idx],
                        score=float(scores[idx])
                    )
                )
    
            return results

    def save(self, path: Path):

        with open(path, "wb") as f:
            pickle.dump(
                {
                    "index": self.index,
                    "chunks": self.chunks
                },
                f
            )

    def load(self, path: Path):

        with open(path, "rb") as f:
            data = pickle.load(f)

        self.index = data["index"]
        self.chunks = data["chunks"]