from app.retrieval.indexer import QdrantIndexer


def test_qdrant_indexer():

    indexer = QdrantIndexer()

    indexer.create_collection(1024)

    collections = indexer.client.get_collections()

    names = [
        c.name
        for c in collections.collections
    ]

    assert "argus_documents" in names