from pathlib import Path

from app.retrieval.models import RawDocument


class DocumentLoader:
    def __init__(self, data_directory: Path):
        self.data_directory = data_directory

    def load(self) -> list[RawDocument]:
        documents = []

        for file_path in self.data_directory.rglob("*.txt"):

            text = file_path.read_text(
                encoding='utf-8',
                errors='ignore'
            )

            document = RawDocument(
                document_id=file_path.stem,
                source_path=file_path,
                text=text
            )

            documents.append(document)

        return documents