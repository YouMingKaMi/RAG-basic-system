from fastapi import HTTPException, UploadFile # type: ignore
from pathlib import Path
import uuid
from app.repositories.document_repository import create_document, search_all_document, search_one_document, create_chunks, delete_chunks, update_document_status, search_chunks_by_keyword, get_chunks_by_document
from app.parser.text_parser import text_parser
from app.chunkers.text_chunker import chunk_text

ALLOWED_EXTENSIONS = [".txt", ".md"]

def allowed_file(filename: str) -> bool:
        return any(
        filename.endswith(ext)
        for ext in ALLOWED_EXTENSIONS
    )

async def process_uploaded(file: UploadFile) -> tuple[bytes, str]:
    filename = file.filename

    if not allowed_file(filename):
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .md files are allowed"
        )
    
    content_bytes = await file.read()

    if len(content_bytes) == 0:
        raise HTTPException(
            status_code =400,
            detail="File is empty"
        )
    
    try:
        content_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be valid UTF-8 text"
        )

    return content_bytes, content_text


async def upload_file(file: UploadFile) -> int:
     content_bytes, content_text = await process_uploaded(file)

     filename = file.filename
     path = Path(filename)

     ext = path.suffix
     unique_id = uuid.uuid4().hex
     stored_filename = unique_id + ext

     upload_dir = Path("storage/uploads")/stored_filename
     upload_dir.write_bytes(content_bytes)
     final_dir = str(upload_dir)


     original_filename = filename
     stored_filename = stored_filename
     stored_path = final_dir
     file_size = len(content_bytes)
     status = "uploaded"

     document_id = create_document(original_filename, stored_filename, stored_path, file_size, status)

     return document_id

def list_documents_service():
     return search_all_document()

def get_doc_service(document_id: int):
     return search_one_document(document_id)

def parse_and_chunk(document_id: int):
    try:
        result = search_one_document(document_id)
        if result is None:
             return "Unable to find the document_id!!!"
        text = text_parser(result["stored_path"])
        chunks = chunk_text(text, chunk_size=50, overlap=10)
        delete_chunks(document_id)
        create_chunks(document_id, chunks)
    except Exception as e: 
         update_document_status(document_id, "failed")
         print(f"Chunked failed: {e}!!!")
    else:
         update_document_status(document_id, "chunked")
         print(f"totoal chunks: {len(chunks)}") 

def keyword_search(keyword:str):
     return search_chunks_by_keyword(keyword)

def get_document_chunks(document_id: int):
     return get_chunks_by_document(document_id)
     


