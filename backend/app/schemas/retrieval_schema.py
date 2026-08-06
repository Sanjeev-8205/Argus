from pydantic import BaseModel

class RetrievalRequest(BaseModel):

    query: str

class RetrievedChunk(BaseModel):

    document_id: str
    chunk_id: str
    chunk_index: int
    department: str
    text: str
    score: float

class RetrievalResponse(BaseModel):

    result: list[RetrievedChunk]