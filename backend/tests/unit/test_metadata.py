from pathlib import Path

from app.retrieval.metadata import MetadataExtractor
from app.retrieval.cleaning import TextCleaner
from app.retrieval.models import RawDocument

def test_department_extraction():

    file_path = Path("data/raw/hr/vacation_policy.txt")
    raw = RawDocument(
        document_id="1",
        source_path=file_path,
        text=file_path.read_text(encoding='utf-8')
    )

    cleaner = TextCleaner()
    cleaned_document = cleaner.clean(raw)

    enriched_document = MetadataExtractor().extract(cleaned_document)

    assert enriched_document.metadata.department=="hr"