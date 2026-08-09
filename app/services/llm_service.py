import ollama

def ollama_chat_process(prompt: str)->str:
    response = ollama.chat(
        model="qwen3:4b-instruct",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    return response.message.content
