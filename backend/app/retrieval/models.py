from dataclasses import dataclass
from pathlib import Path

@dataclass
class RawDocument:
    document_id: int
    source_path: Path
    text: str