from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .retrieval.vector_store import get_index
# from .retrieval.query_intelligence import enhance_query
from .retrieval.retriever import retrieve
from .retrieval.ranker import rerank
from .llm.generator import generate_answer
from .utils.cache import query_cache

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

index = get_index()


from app.schemas import QueryRequest
from .retrieval.query_intelligence import contextualize_query

@app.post("/query")
def query_api(request: QueryRequest):
    query = request.query
    history = request.history


    if history:
        query = contextualize_query(query, history)

    cached = query_cache.get(query)
    if cached:
        return cached


    nodes = retrieve(index, query, top_k=10)
    ranked = rerank(query, nodes)

    if ranked:
        top_context = "\n".join([node.text for _, node in ranked[:3]])
    else:
        top_context = ""

    answer = generate_answer(query, top_context, history)

    response = {
        "answer": answer,
        "scores": []
    }
    

    query_cache.set(query, response)
    
    return response
