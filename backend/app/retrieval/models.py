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

@dataclass
class DocumentChunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    metadata: DocumentMetadata

@dataclass
class EmbeddedChunk:
    chunk: DocumentChunk
    embedding: list[float]

@dataclass
class IngestionResult:
    documents_processed: int
    chunks_created: int
    embeddings_generated: int