from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from qdrant_client import QdrantClient
from app.config import settings

def get_index():
    client = QdrantClient(url=settings.QDRANT_URL)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=settings.COLLECTION_NAME,
        enable_hybrid=False,
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    return VectorStoreIndex.from_vector_store(vector_store)
