from pathlib import Path

from app.retrieval.models import (
    CleanDocument, DocumentMetadata, EnrichedDocument
)

class MetadataExtractor:

    def extract(self, document: CleanDocument) -> EnrichedDocument:

        metadata = DocumentMetadata()

        metadata.department = self._extract_department(
            document.source_path
        )

        return EnrichedDocument(
            document_id=document.document_id,
            source_path=document.source_path,
            text=document.text,
            metadata=metadata
        )


    def _extract_department(self, path: Path) -> str | None:

        parts = [p.lower() for p in path.parts]

        departments = {
            "hr", "finance", "engineering", "legal", "executive", "public"
        }

        for part in parts:
            if part in departments:
                return part
        
        return None