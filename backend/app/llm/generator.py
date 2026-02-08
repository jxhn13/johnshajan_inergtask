import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
client = genai.GenerativeModel('gemini-2.5-flash')

from typing import List, Optional
from app.schemas import Message

def generate_answer(query: str, context: str, history: List[Message] = None):
    history_text = ""
    if history:
        # Format history as a string
        history_str = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
        history_text = f"Chat History:\n{history_str}\n"

    prompt = f"""
    Use the context below to answer accurately.
    Format the response in a clear, structured way.
    - Do NOT use bolding (**) or italics.
    - Do NOT use markdown lists if they clutter the view.
    - Use clear headings and line breaks.
    - Keep it professional and concise.

    {history_text}
    Context:
    {context}

    Question:
    {query}
    """

    response = client.generate_content(prompt)

    return response.text
