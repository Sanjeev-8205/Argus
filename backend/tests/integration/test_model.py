from sentence_transformers import SentenceTransformer


def test_model():
    model = SentenceTransformer(
        "BAAI/bge-large-en-v1.5"
    )

    assert model is not None