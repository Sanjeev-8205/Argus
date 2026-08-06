from fastapi import APIRouter, Request

from app.schemas.retrieval_schema import RetrievalRequest, RetrievedChunk, RetrievalResponse
from app.services.retrieval_service import RetrievalService

router = APIRouter(
    prefix="/retrieval",
    tags=['Retrieval']
)

retrieval_service = RetrievalService()

@router.post("/search", response_model=RetrievalResponse)
async def retrieve(request: Request, body: RetrievalRequest):
    service = request.app.state.retrieval_service

    results = service.retrieve(
        body.query
    )

    response = []

    for result in results:
        response.append(
            RetrievedChunk(
                document_id=result.chunk.document_id,
                chunk_id=result.chunk.chunk_id,
                chunk_index=result.chunk.chunk_index,
                department=result.chunk.metadata.department,
                text=result.chunk.text,
                score=result.score
            )
        )

    return RetrievalResponse(
        result=response
    )
