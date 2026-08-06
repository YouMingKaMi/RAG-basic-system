import chromadb
from app.services.embedding_service import ollama_embedding_process

client = chromadb.EphemeralClient()

collection = client.get_or_create_collection(
    name = "test"
)

documents = ["我爱温水佳树", "编程真好玩","卧槽原"]

embeddings = [ollama_embedding_process(document) for document in documents]

collection.add(
    ids=["test1","test2","test3"],
    embeddings=embeddings,
    metadatas = [{"category":"anime","character":"lover"},{"category":"coding"},{"category":"game"}],
    documents=documents
)

new_document = "这是一条试图覆盖 test1 的新文本"
new_embedding = ollama_embedding_process(new_document)

collection.add(
    ids=["test1"],
    documents=[new_document],
    embeddings=[new_embedding],
    metadatas=[{"category": "new"}],
)

questions = ["我最爱的人", "有什么好玩的东西"]

query_embeddings = [ollama_embedding_process(question) for question in questions]

result = collection.query(
    query_embeddings=query_embeddings,
    include=["metadatas","documents","distances"],
    n_results=2
)

print(result["metadatas"])
print(result["documents"])
print(result["distances"])