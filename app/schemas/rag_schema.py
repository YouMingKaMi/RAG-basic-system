from pydantic import BaseModel, Field

class RagRequest(BaseModel):
    question: str = Field(min_length=1,max_length=500)

class QuoteResponse(BaseModel):
    content: str
    document_id: int
    chunk_id: int
    distance: float

class RagResponse(BaseModel):
    answer: str
    sources: list[QuoteResponse]

class RagSessionRequest(RagRequest):
    session_id: int | None = None

class RagSessionResponse(RagResponse):
    session_id: int