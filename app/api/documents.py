from fastapi import APIRouter, UploadFile, File
from app.services.document_service import upload_file, list_documents_service, get_doc_service, parse_and_chunk
from app.services.indexing_service import index_by_id
from app.schemas.document_schema import DocumentResponse, DocumentListResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/",response_model=DocumentListResponse)
def list_documents():
    return list_documents_service()

@router.post("/upload", status_code=201, response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
     document_id = await upload_file(file)
     parse_and_chunk(document_id)
     index_by_id(document_id)
     return get_doc_service(document_id)


@router.get("/get_docs/{document_id}", response_model=DocumentResponse)
def get_doc(document_id: int):
    return get_doc_service(document_id)
