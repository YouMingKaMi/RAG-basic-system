import chromadb
from app.services.embedding_service import ollama_embedding_process

client = chromadb.PersistentClient(
    path="storage/chroma_experiment"
)

collection = client.get_collection(
    name="real_test"
)

questions = ["和小丑相关的动画","和告别相关的动画"]
query_embeddings = [ollama_embedding_process(question) for question in questions] 
result = collection.query(
    query_embeddings=query_embeddings,
    n_results=1,
    include=["documents","distances"]
)

print(result["documents"])
print(result["distances"])