from app.repositories.document_repository import get_chunks_by_document, update_document_status, get_connection
from app.services.embedding_service import ollama_embedding_process
from app.services.chroma_service import upsert_document_vectors
from app.exceptions import IndexProcessError

def index_by_id(document_id: int):
    conn = get_connection()
    try:
        chunks = get_chunks_by_document(document_id)
        if not chunks:
            raise ValueError()
        update_document_status(conn, document_id, "indexing")
        conn.commit()

        embeddings = [ollama_embedding_process(chunk["content"]) for chunk in chunks]
        chunk_ids = [chunk["chunk_id"] for chunk in chunks]
        full_ids = []
        metadatas = []
        for chunk_id in chunk_ids:
            full_id = f"doc_{document_id}_chunk_{chunk_id}"
            metadata = {"document_id":document_id, "chunk_id":chunk_id}
            full_ids.append(full_id)
            metadatas.append(metadata)
        success =  upsert_document_vectors(document_id, full_ids, embeddings, metadatas)
        if not success: 
             raise RuntimeError(f"Vectors indexing failed, document_id : {document_id}")
        update_document_status(conn, document_id, "indexed")
        conn.commit()
    except Exception:       
            update_document_status(conn, document_id, "index_failed")
            conn.commit()
            raise IndexProcessError(
                 "Index process failed!!!"
            )
    finally:
         conn.close()

if __name__ == "__main__":
    index_by_id(20)
      



    
    
    
    
