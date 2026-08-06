import hashlib
import ollama

def mock_embedding_test(content: str)->list[float]:
    if not content.strip():
        raise ValueError("Content cannot be empty!!")
    result = hashlib.sha256(content.encode("utf-8")).hexdigest()
    corr_hex = []
    corr = []

    for start in range(0,len(result),8):
        corr_hex.append(result[start:start+8])
    for start in range(0,8):
        total_value = 0
        current_corr = corr_hex[start]
        for a in range(0,8):
            if current_corr[a] in ['a','b','c','d','e','f']:
                value = ord(current_corr[a]) - 87
            else:
                value = int(current_corr[a])
            total_value += value*16**(3-a)
        corr.append(float(total_value))
    return corr

def ollama_embedding_process(content: str)->list[float]:
    if not content.strip():
        raise ValueError("The content should not empty")
    ollama_response = ollama.embed(
        model="qwen3-embedding:0.6b",
        input=content
    )
    vector = ollama_response.embeddings[0]
    return vector