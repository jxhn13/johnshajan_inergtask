import os
from dotenv import load_dotenv

from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings
import google.generativeai as genai

load_dotenv()

class AppSettings:
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET")

    QDRANT_URL = os.getenv("QDRANT_URL")
    COLLECTION_NAME = "insurance_docs"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = AppSettings()

# Configure LlamaIndex
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Use Local Embeddings 
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash",
    api_key=settings.GEMINI_API_KEY
)
