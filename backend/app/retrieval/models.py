from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class DocumentMetadata:
    department: str | None = None
    sender: str | None = None
    recipients: list[str] = field(default_factory=list)
    subject: str | None = None
    date: str | None = None

@dataclass
class RawDocument:
    document_id: str
    source_path: Path
    text: str

@dataclass
class CleanDocument:
    document_id: str
    source_path: Path
    text: str

@dataclass
class EnrichedDocument:
    document_id: str
    source_path: Path
    text: str
    metadata: DocumentMetadata