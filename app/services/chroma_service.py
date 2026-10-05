import chromadb
from app.config import CHROMA_PATH, COLLECTION_NAME

def upsert_document_vectors(document_id:int, ids:list, embeddings:list, metadatas:list, collection_name: str = COLLECTION_NAME)-> bool:
    try:
        client = chromadb.PersistentClient(
            path = CHROMA_PATH
        )
        collection = client.get_or_create_collection(
            name = collection_name
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

def search_vector(question_embedding: list[float], collection_name: str = COLLECTION_NAME, top_k: int = 3):
    client = chromadb.PersistentClient(
        path = CHROMA_PATH
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

def delete(document_id: int, collection_name: str):
    client = chromadb.PersistentClient(
        path = CHROMA_PATH
    )
    collection = client.get_or_create_collection(
        name=collection_name
    )
    collection.delete(
        where={
            "document_id": document_id
        }
    )

