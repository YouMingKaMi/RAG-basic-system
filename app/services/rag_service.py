from app.services.retrieval_service import retrieve
from app.services.llm_service import ollama_temporary_chat_process, ollama_long_chat_process
from app.repositories.document_repository import get_session_content, add_session_content, create_new_session
import logging

logger = logging.getLogger(__name__)

def build_rag_prompt(question:str, contexts: list)-> str:
    context_content = []
    for context in contexts:
        context_content.append(context["content"])
    prompt = f"你是一个RAG文档助手， 负责根据以下给你的背景信息来回答用户问题，如果在文档中找不到相关信息，则拒绝回答。如果背景信息只能部分回答问题，或者回答问题还需要用户提供额外信息，应明确指出缺少的信息，而不是自行假设。\n背景信息如下:{context_content}\n 用户问题如下:{question}"
    return prompt

def rag_service(question: str):
    contexts = retrieve(question,collection_name="personal_documents")
    if not contexts:
        logger.warning(f"Rejected question(no context return above the threshold):{question!r}")
        answer ="抱歉，该问题本文档暂无记载"
        return answer, contexts
    prompt = build_rag_prompt(question, contexts)
    answer = ollama_temporary_chat_process(prompt)
    return answer,contexts

def rag_session_service(question: str, session_id: int):
    if session_id is None:
        session_id = create_new_session()
    contexts = retrieve(question,collection_name="personal_documents")
    if not contexts:
        answer ="抱歉，该问题本文档暂无记载"
        logger.warning(f"Rejected question(no context return above the threshold):{question!r}, session_id={session_id}")
        return answer, contexts, session_id
    prompt = build_rag_prompt(question, contexts)
    messages = get_session_content(session_id) 
    response, answer_dict, question_dict= ollama_long_chat_process(messages, prompt)
    add_session_content(session_id, question_dict, answer_dict)

    return response,contexts,session_id
 