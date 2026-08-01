import re
from app.retrieval.models import RawDocument, CleanDocument

class TextCleaner:
    def clean(self, document: RawDocument) -> CleanDocument:

        text = document.text

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        text = text.replace("\t", " ")

        text = re.sub(r"[ ]{2,}", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        text = text.strip()

        return CleanDocument(
            document_id=document.document_id,
            source_path=document.source_path,
            text=text
        )