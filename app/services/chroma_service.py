import chromadb

def upsert_document_vectors(document_id:int, ids:list, embeddings:list, metadatas:list)-> bool:
    try:
        client = chromadb.PersistentClient(
            path = "storage/chroma_experiment"
        )
        collection = client.get_or_create_collection(
            name="personal_documents"
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
        print(e)
        return False
