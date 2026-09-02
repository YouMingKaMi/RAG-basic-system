from fastapi import APIRouter 
from app.services.document_service import keyword_search, get_document_chunks
from app.services.rag_service import rag_service, rag_session_service
from app.schemas.rag_schema import RagRequest, RagResponse, RagSessionRequest, RagSessionResponse
from app.schemas.document_schema import DocuemntChunksResponse, KeywordSearchResponse


router = APIRouter(prefix="/search", tags=["search"])

@router.get("/keywords/{keyword}", response_model=KeywordSearchResponse)
def keyword_find(keyword: str):
    return keyword_search(keyword)

@router.get("/document_id/{document_id}", response_model=DocuemntChunksResponse)
def document_id_search(document_id: int):
    return get_document_chunks(document_id)

@router.post("/rag/temporary_chat",response_model= RagResponse)
def temporary_chat(request: RagRequest):
    answer, sources = rag_service(request.question)
    return RagResponse(answer=answer,sources=sources)

@router.post("/rag/long_chat",response_model=RagSessionResponse)
def long_chat(request: RagSessionRequest):
    question, session_id = request.question, request.session_id
    answer, sources, session_id = rag_session_service(question, session_id)
    return RagSessionResponse(answer=answer, sources=sources, session_id=session_id)

