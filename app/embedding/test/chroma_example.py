import chromadb

from app.services.embedding_service import ollama_embedding_process


client = chromadb.EphemeralClient()

collection = client.get_or_create_collection(
    name="embedding_experiment"
)


documents = [
    "猫正在吃鱼",
    "SQLite用于保存结构化数据",
    "员工出差前需要提交审批",
]

embeddings = [
    ollama_embedding_process(document)
    for document in documents
]


collection.add(
    ids=["text-1", "text-2", "text-3"],
    documents=documents,
    embeddings=embeddings,
    metadatas=[
        {"category": "animal"},
        {"category": "database"},
        {"category": "company_policy"},
    ],
)


questions = ["猫最喜欢吃什么？","公司出差的流程是什么？"]
question_embedding = [ollama_embedding_process(question) for question in questions]


results = collection.query(
    query_embeddings=question_embedding,
    n_results=2,
    include=["documents", "metadatas", "distances"],
)


print(type(results))
print(results.keys())
print(results["ids"])
print(results["documents"])
print(results["metadatas"])
print(results["distances"])