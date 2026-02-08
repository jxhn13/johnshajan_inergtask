import google.generativeai as genai
from app.config import settings

_client = None

def _get_client():
    global _client
    if _client is None:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _client = genai.GenerativeModel('gemini-2.5-flash')
    return _client


from typing import List
from app.schemas import Message

def contextualize_query(query: str, history: List[Message]) -> str:
    if not history:
        return query

    prompt = f"""
    Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.

    Chat History:
    {history}

    Latest Question: {query}
    """

    client = _get_client()
    response = client.generate_content(prompt)

    return response.text
