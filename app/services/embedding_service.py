import ollama

def ollama_embedding_process(content: str)->list[float]:
    if not content.strip():
        raise ValueError("The content should not empty")
    ollama_response = ollama.embed(
        model="qwen3-embedding:0.6b",
        input=content
    )
    vector = ollama_response.embeddings[0]
    return vector