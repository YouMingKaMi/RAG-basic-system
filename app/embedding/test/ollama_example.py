import ollama

response1 = ollama.embed(
    model="qwen3-embedding:0.6b",
    input="猫正在吃鱼"
)

response2 = ollama.embed(
    model="qwen3-embedding-error",
    input="我讨厌猫"
)


vector1 = response1.embeddings[0]
vector2 = response2.embeddings[0]

print(vector1 == vector2)


