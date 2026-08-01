from dataclasses import dataclass
from pathlib import Path

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