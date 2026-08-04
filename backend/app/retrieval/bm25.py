from rank_bm25 import BM25Okapi

from app.retrieval.models import DocumentChunk

class BM25Indexer:

    def __init__(self):

        self.index = None
        self.chunks = []

    def build(self, chunks: list[DocumentChunk]):

        corpus = [
            chunk.text.lower().strip()
            for chunk in chunks
        ]

        self.index = BM25Okapi(corpus)
        self.chunks = chunks

        print(f"Corpus:\n{corpus}\n\nIndex:\n{self.index}\n\nChunks:\n{self.chunks}")