from fastapi import APIRouter, UploadFile, File # type: ignore
from app.services.document_service import upload_file, list_documents_service, get_doc_service, parse_and_chunk

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/")
def list_documents():
    return {"documents": list_documents_service()}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    document_id = await upload_file(file)
    parse_and_chunk(document_id)



@router.get("/get_doc")
def get_doc(document_id: int):
    return get_doc_service(document_id)
