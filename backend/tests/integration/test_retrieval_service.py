from app.services.retrieval_service import RetrievalService

def test_retrieval_service():

    retrieval_service = RetrievalService()

    results = retrieval_service.retrieve(
        "cash flow and budget approval policy"
    )

    assert len(results) > 0
    assert len(results) == 5
    assert results[0].score > 0
    assert results[0].score >= results[-1].score
