import ollama
from app.repositories.document_repository import get_session_content, add_session_content, create_new_session

def ollama_temporary_chat_process(prompt: str)->str:
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

def ollama_long_chat_process(messages: list[dict], prompt: str):
    question_dict = {
        "role":"user",
        "content":prompt
    }
    messages.append(question_dict)
    response = ollama.chat(
        model="qwen3:4b-instruct",
        messages = messages
    )
    answer_dict = {
        "role":response.message["role"],
        "content": response.message["content"]
    }
    return response.message.content, answer_dict, question_dict
