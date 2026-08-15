from mcp.server import MCPServer

from app.services.retrieval_service import RetrievalService

mcp = MCPServer("argus_server")

retrieval_service = RetrievalService()

@mcp.tool(
    description=(
            "Search the organization's indexed documents for information "
            "relevant to the user's query. Returns ranked document chunks "
            "with metadata and relevance scores."
        )
    )
def retrieve_documents(query: str) -> list[dict]:

    results = retrieval_service.retrieve(query)

    return [
        {
            "document_id": result.chunk.document_id,
            "chunk_id": result.chunk.chunk_id,
            "chunk_index": result.chunk.chunk_index,
            "department": result.chunk.metadata.department,
            "text": result.chunk.text,
            "score": result.score
        }

        for result in results
    ]

if __name__ == "__main__":
    mcp.run()