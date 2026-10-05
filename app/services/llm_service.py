from openai import OpenAI
from app.config import KIMI_API_KEY, AI_URL, CHAT_MODEL

client = OpenAI(base_url=AI_URL,api_key=KIMI_API_KEY)

def temporary_chat_process(prompt: str)->str:
    messages = [{"role":"user","content":prompt}]
    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        timeout=60.0,
    )
    return completion.choices[0].message.content

def long_chat_process(messages: list[dict], prompt: str):
    question_dict = {
        "role":"user",
        "content":prompt
    }
    messages.append(question_dict)
    complection = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        timeout=60.0
    )
    answer_dict = {
        "role":complection.choices[0].message.role,
        "content": complection.choices[0].message.content
    }
    return complection.choices[0].message.content, answer_dict, question_dict
