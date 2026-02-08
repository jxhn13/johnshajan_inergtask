def retrieve(index, query: str, top_k: int = 5):
    retriever = index.as_retriever(similarity_top_k=top_k)
    return retriever.retrieve(query)
