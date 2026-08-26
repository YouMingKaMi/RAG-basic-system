from app.services.retrieval_service import retrieve
from app.services.llm_service import ollama_chat_process


def build_rag_prompt(question:str, contexts: list)-> str:
    context_content = []
    for context in contexts:
        context_content.append(context["content"])
    prompt = f"你是一个RAG文档助手， 负责根据以下给你的背景信息来回答用户问题，如果在文档中找不到相关信息，则拒绝回答。如果背景信息只能部分回答问题，或者回答问题还需要用户提供额外信息，应明确指出缺少的信息，而不是自行假设。\n背景信息如下:{context_content}\n 用户问题如下:{question}"
    return prompt

def rag_service(question: str):
    contexts = retrieve(question,collection_name="personal_documents")##记住未来去掉
    prompt = build_rag_prompt(question, contexts)
    answer = ollama_chat_process(prompt)
    return answer