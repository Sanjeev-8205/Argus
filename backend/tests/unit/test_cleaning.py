from pathlib import Path

from app.retrieval.cleaning import TextCleaner
from app.retrieval.models import RawDocument

def test_text_cleaner():

    raw = RawDocument(
        document_id="1",
        source_path=Path("data/raw/sample.txt"),
        text="Hello     World\r\n\r\n\r\nNext\tLine"
    )

    cleaner = TextCleaner()

    cleaned = cleaner.clean(raw)

    assert cleaned.text=="Hello World\n\nNext Line"