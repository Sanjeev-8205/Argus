from pathlib import Path

from app.retrieval.ingest import DocumentLoader

loader = DocumentLoader(
    data_directory=Path("data/raw")
)

documents = loader.load()

print(f"Loaded {len(documents)} documents.")

for document in documents:
    print(document.document_id)
    print(document.source_path)
    print(document.text)