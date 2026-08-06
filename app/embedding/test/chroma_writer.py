import chromadb
from app.services.embedding_service import ollama_embedding_process

client = chromadb.PersistentClient(
    path='storage/chroma_experiment'
)

collection = client.get_or_create_collection(
    name="personal_documents"
)

ids = ["anime1","anime2"]
documents = ["向日葵马戏团","再见拉拉"]
embeddings = [ollama_embedding_process(document) for document in documents]
metadatas = [{"type":"日常","wife":"女主"},{"type":"剧情","wife":"菈菈"}]

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print(collection.count())