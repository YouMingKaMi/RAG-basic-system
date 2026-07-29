from fastapi import APIRouter #type: ignore
from app.services.document_service import keyword_search, get_document_chunks
router = APIRouter(prefix="/search", tags=["search"])

@router.get("/keywords/{keyword}")
def keyword_search(keyword: str):
    return keyword_search(keyword)

@router.get("/document_id/{document_id}")
def document_id_search(document_id: int):
    return get_document_chunks(document_id)