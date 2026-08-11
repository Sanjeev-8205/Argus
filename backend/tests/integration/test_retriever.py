from app.retrieval.retriever import DenseRetriever


def test_dense_retriever():

    retriever = DenseRetriever()

    results = retriever.retrieve(
        "Company Policy", topk=3
    )

    assert len(results) > 0
    assert results[0].score > 0
    assert results[0].chunk.text != ""