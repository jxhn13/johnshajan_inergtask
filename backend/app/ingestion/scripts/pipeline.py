import time
import logging
from app.ingestion.minio_client import get_minio_client
from app.ingestion.extractor import extract_text_from_pdf
from app.ingestion.chunker import chunk_text
from app.config import settings
from app.retrieval.vector_store import get_index
from llama_index.core.schema import TextNode
from qdrant_client import QdrantClient

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ingestion():
    logger.info("--- Starting Full Ingestion Pipeline ---")
    
    # 1. Connect to MinIO
    logger.info(f"Connecting to MinIO at {settings.MINIO_ENDPOINT}...")
    try:
        minio_client = get_minio_client()
        if not minio_client.bucket_exists(settings.MINIO_BUCKET):
             logger.error(f"Bucket '{settings.MINIO_BUCKET}' does not exist.")
             return
    except Exception as e:
        logger.error(f"MinIO Connection Failed: {e}")
        return

    # 2. List Objects
    logger.info("Listing PDF files...")
    try:
        objects = list(minio_client.list_objects(settings.MINIO_BUCKET, recursive=True))
        pdf_objects = [obj for obj in objects if obj.object_name.endswith('.pdf')]
        logger.info(f"Found {len(pdf_objects)} PDF files to process.")
        
        if not pdf_objects:
            logger.warning("No PDF files found.")
            return
            
    except Exception as e:
        logger.error(f"Listing Objects Failed: {e}")
        return

    # 3. Initialize Vector Store
    logger.info("Initializing Vector Store Index...")
    try:
        index = get_index()
    except Exception as e:
        logger.error(f"Index Init Failed: {e}")
        return

    # 4. Process Files
    logger.info("Processing Files...")
    total_chunks_inserted = 0
    
    for i, pdf_obj in enumerate(pdf_objects):
        filename = pdf_obj.object_name
        logger.info(f"Processing ({i+1}/{len(pdf_objects)}): {filename}")
        
        try:
            # Download
            response = minio_client.get_object(settings.MINIO_BUCKET, filename)
            pdf_bytes = response.read()
            response.close()
            response.release_conn()
            
            # Extract
            text = extract_text_from_pdf(pdf_bytes)
            if not text.strip():
                logger.warning(f"   ⚠ Skipped: No text extracted from {filename}")
                continue
            
            # Chunk
            chunks = chunk_text(text)
            if not chunks:
                logger.warning(f"   ⚠ Skipped: No chunks created for {filename}")
                continue
                
            logger.info(f"   -> Extracted {len(text)} chars, created {len(chunks)} chunks.")
            
            # Create Nodes
            nodes = [TextNode(text=chunk, metadata={"filename": filename}) for chunk in chunks]
            
            # Insert (Local Embeddings = No Rate Limits)
            index.insert_nodes(nodes)
            total_chunks_inserted += len(chunks)
            logger.info(f"   ✅ Inserted {len(chunks)} vectors.")
            
        except Exception as e:
            logger.error(f"   ❌ Failed to process file {filename}: {e}")

    # 5. Summary
    logger.info("✅ Ingestion Complete.")
    logger.info(f"Vectors added this run: {total_chunks_inserted}")

if __name__ == "__main__":
    run_ingestion()
