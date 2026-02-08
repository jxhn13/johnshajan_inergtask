import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
client = genai.GenerativeModel('gemini-2.5-flash')

import json

def rerank(query, nodes):
    if not nodes:
        return []


    documents_str = ""
    for i, node in enumerate(nodes):
        text_preview = node.text[:500].replace("\n", " ") 
        documents_str += f"[{i}] {text_preview}\n"

    prompt = f"""
    You are a ranking engine.
    Query: {query}
    
    Documents:
    {documents_str}
    
    Rank these documents by relevance to the query.
    Return a valid JSON list of objects, where each object has 'index' (0-{len(nodes)-1}) and 'score' (0-100).
    Example: [{{"index": 1, "score": 95}}, {{"index": 0, "score": 40}}]
    Only return the JSON.
    """

    try:
        res = client.generate_content(prompt)
        text = res.text.replace("```json", "").replace("```", "").strip()
        rankings = json.loads(text)
        
        scored = []
        for item in rankings:
            idx = item.get("index")
            score = item.get("score")
            if idx is not None and 0 <= idx < len(nodes):
                scored.append((score, nodes[idx]))
        

        scored.sort(reverse=True, key=lambda x: x[0])
        return scored

    except Exception as e:
        print(f"Reranking failed: {e}")
        return [(0.5, node) for node in nodes]
