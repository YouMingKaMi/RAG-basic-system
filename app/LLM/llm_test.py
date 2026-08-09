import ollama

response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role":"user",
            "content":"你是谁"
        }
    ]
)

print(type(response))
print(response)
print(response.message.content)