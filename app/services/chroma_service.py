import chromadb

def upsert_document_vectors(document_id:int, ids:list, embeddings:list, metadatas:list, collection_name: str ="personal_documents")-> bool:
    try:
        client = chromadb.PersistentClient(
            path = "storage/chroma_experiment"
        )
        collection = client.get_or_create_collection(
            name=collection_name
        )
        collection.delete(
            where={
                "document_id": document_id
            }
        )
        collection.upsert(
            embeddings = embeddings,
            ids = ids,
            metadatas= metadatas
        )
        return True
    except Exception as e:
        if "collection" in locals():
            collection.delete(
                where={
                    "document_id": document_id
                }
            )
        return False

def search_vector(question_embedding: list[float], collection_name: str = "personal_documents", top_k: int = 3):
    client = chromadb.PersistentClient(
        path="storage/chroma_experiment"
    )
    collection = client.get_collection(
        name=collection_name
    )
    result = collection.query(
        query_embeddings=question_embedding,
        n_results=top_k,
        include=["metadatas","distances"]
    )
    return result
