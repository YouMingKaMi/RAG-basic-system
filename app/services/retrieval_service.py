from app.services.embedding_service import ollama_embedding_process
from app.services.chroma_service import search_vector
from app.repositories.document_repository import get_chunk_content

def retrieve(question:str, top_k:int =3, collection_name: str ="personal_documents"):
    question_embedding = ollama_embedding_process(question)
    vector_double_list = search_vector(question_embedding, collection_name, top_k)

    [vector_list] = vector_double_list["metadatas"]
    [distances] = vector_double_list["distances"]
    content_list = []
    for metadata, distance in zip(vector_list,distances):
        if distance > 1.4:
            continue
        if (content:=get_chunk_content(metadata["document_id"], metadata["chunk_id"])) is None:
            raise LookupError(f"Chunk not found: document_id={metadata['document_id']}, chunk_id={metadata['chunk_id']} ")
        content_list.append({"content": content,
                             "document_id":metadata["document_id"],
                             "chunk_id":metadata["chunk_id"],
                             "distance":distance})
    return content_list

    







    

