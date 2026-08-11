from app.retrieval.qdrant import get_qdrant_client


def test_qdrant_client():
    client = get_qdrant_client()

    collections = client.get_collections()

    assert collections is not None