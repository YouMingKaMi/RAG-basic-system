from fastapi import UploadFile # type: ignore
from pathlib import Path
import uuid
from app.repositories.document_repository import create_document, search_all_document, search_one_document, create_chunks, delete_chunks, update_document_status, search_chunks_by_keyword, get_chunks_by_document, get_connection
from app.parser.text_parser import text_parser
from app.chunkers.text_chunker import chunk_text
from app.exceptions import DocumentNotFoundError, InvalidUploadError, UploadProcessError, ChunkProcessError

ALLOWED_EXTENSIONS = [".txt", ".md"]

def allowed_file(filename: str) -> bool:
        return any(
        filename.endswith(ext)
        for ext in ALLOWED_EXTENSIONS
    )

async def process_uploaded(file: UploadFile) -> tuple[bytes, str]:
    filename = file.filename

    if not allowed_file(filename.lower()): 
        raise InvalidUploadError(
            "Only .txt and .md files are allowed"
        )
    
    content_bytes = await file.read()

    if len(content_bytes) == 0: 
        raise InvalidUploadError(
            "File is empty"
        )
    if len(content_bytes) > 5*1024*1024:
         raise InvalidUploadError(
              "File exceeds the 5MB size limit"
         )
    
    try:
        content_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise InvalidUploadError(
            "File must be valid UTF-8 text"
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

     try:
        upload_dir.write_bytes(content_bytes)
        stored_path = str(upload_dir)

        file_size = len(content_bytes)
        status = "uploaded"

        document_id = create_document(filename, stored_filename, stored_path, file_size, status)

        return document_id
     except Exception:
        if upload_dir.exists():
            upload_dir.unlink()
        raise UploadProcessError(
             "Upload process failed!!!"
        )

          

def list_documents_service():
     documents = search_all_document()
     return {
          "documents": documents,
          "count": len(documents)
     }

def get_doc_service(document_id: int):
     content = search_one_document(document_id)
     return content
def parse_and_chunk(document_id: int):
    result = search_one_document(document_id)
    if result is None:
          raise DocumentNotFoundError(
               f"This {document_id} is not available!!"
          )
    conn = get_connection()
    try:
        text = text_parser(result["stored_path"])
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        delete_chunks(conn, document_id)
        create_chunks(conn, document_id, chunks)
        update_document_status(conn, document_id, "chunked")
        conn.commit()
        print(f"totoal chunks: {len(chunks)}") 
    except Exception: 
         conn.rollback()
         update_document_status(conn, document_id, "failed")
         conn.commit()
         raise ChunkProcessError(
              "Chunk process failed!!!"
         )
    finally:
         conn.close()


def keyword_search(keyword:str):
     content = search_chunks_by_keyword(keyword)
     return {
          "keyword":keyword,
          "results": content,
          "count": len(content)
          }

def get_document_chunks(document_id: int):
     content = get_chunks_by_document(document_id)
     if not content:
          raise DocumentNotFoundError(
               "Can not found the document by this id"
          )
     return {
          "document_id": document_id,
          "chunks": content,
          "count": len(content)
          }
