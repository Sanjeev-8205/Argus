from pathlib import Path

from app.retrieval.tokenizer import get_tokenizer


def test_tokenizer():
    tokenizer = get_tokenizer()

    text = Path("data/raw/engineering/api.txt").read_text(encoding='utf-8')
    tokens = tokenizer.encode(text)

    assert len(tokens)>0