from app.repositories.document_repository import get_chunks_by_document, update_document_status
from app.services.embedding_service import ollama_embedding_process
from app.services.chroma_service import upsert_document_vectors

def index_by_id(document_id: int):
    chunks = get_chunks_by_document(document_id)
    if not chunks:
        raise ValueError()
    update_document_status(document_id, "indexing")
    embeddings = [ollama_embedding_process(chunk["content"]) for chunk in chunks]
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    full_ids = []
    metadatas = []
    for chunk_id in chunk_ids:
        full_id = f"doc_{document_id}_chunk_{chunk_id}"
        metadata = {"document_id":document_id, "chunk_id":chunk_id}
        full_ids.append(full_id)
        metadatas.append(metadata)
    if upsert_document_vectors(document_id, full_ids, embeddings, metadatas):
        update_document_status(document_id, "indexed")
    else:        
        update_document_status(document_id, "index_failed")

if __name__ == "__main__":
        index_by_id(7)
      



    
    
    
    
