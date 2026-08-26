from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import upload_file, list_documents_service, get_doc_service, parse_and_chunk
from app.services.indexing_service import index_by_id
from app.exceptions import InvalidUploadError, UploadProcessError, ChunkProcessError, IndexProcessError

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/")
def list_documents():
    return {"documents": list_documents_service()}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        document_id = await upload_file(file)
        parse_and_chunk(document_id)
        index_by_id(document_id)
    except InvalidUploadError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    except UploadProcessError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
    except ChunkProcessError as error:
        raise HTTPException(
            status_code=501,
            detail=str(error)
        )
    except IndexProcessError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/get_doc")
def get_doc(document_id: int):
    return get_doc_service(document_id)
