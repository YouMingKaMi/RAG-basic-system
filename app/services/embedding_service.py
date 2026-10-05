from openai import OpenAI
from app.config import EMBED_AI_URL, EMBED_API_KEY, EMBED_MODEL

client = OpenAI(base_url=EMBED_AI_URL, api_key=EMBED_API_KEY, timeout=60.0)

def embedding_process(content: str) -> list[float]:
    if not content.strip():
        raise ValueError("The content should not empty")
    resp = client.embeddings.create(
        input=content,
        model=EMBED_MODEL
    )
    embeddings = resp.data[0].embedding
    return embeddings

