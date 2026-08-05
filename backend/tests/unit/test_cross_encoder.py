from app.retrieval.cross_encoder import get_cross_encoder

def test_cross_encoder():

    cross_encoder = get_cross_encoder()
    
    assert cross_encoder is not None