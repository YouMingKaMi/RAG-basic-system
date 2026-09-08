from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    original_filename: str
    file_size: int
    status: str
    created_at: str

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    count: int

class ChunkContent(BaseModel):
    document_id: int
    chunk_id: int
    content: str
    created_at: str

class DocumentChunksResponse(BaseModel):
    document_id: int
    chunks: list[ChunkContent]
    count: int

class KeywordSearchResponse(BaseModel):
    keyword: str
    results: list[ChunkContent]
    count: int
