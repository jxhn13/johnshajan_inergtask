# Insurance RAG System

This project is a Retrieval-Augmented Generation (RAG) system designed for the insurance domain. It ingests PDF documents, creates embeddings, stores them in a Qdrant vector database, and allows users to query the information via a React.js frontend or a FastAPI backend. It leverages Google's Gemini models for generation and reranking.

## Tech Stack

### Backend
-   **Framework**: FastAPI
-   **Language**: Python 3.12+
-   **Orchestration**: LlamaIndex
-   **Vector Database**: Qdrant
-   **Object Storage**: MinIO
-   **LLM**: Google Gemini (via `google-generativeai`)
-   **Embeddings**: HuggingFace (`BAAI/bge-small-en-v1.5`)
-   **PDF Parsing**: PyPDF2

### Frontend
-   **Interface**: React (Vite)
-   **Communication**: HTTP Requests to Backend

### Infrastructure
-   **Containerization**: Docker & Docker Compose (implied by file structure)

## Prerequisites

-   Python 3.12+
-   Docker & Docker Compose (for MinIO and Qdrant)
-   Google Gemini API Key

## Installation & Setup

1.  **Clone the repository** (if applicable).

2.  **Environment Configuration**:
    Create a `.env` file in `backend/app/.env` (or project root depending on how you run it) with the following variables:
    ```env
    MINIO_ENDPOINT=localhost:9000
    MINIO_ACCESS_KEY=minioadmin
    MINIO_SECRET_KEY=minioadmin
    MINIO_BUCKET=insurance-docs
    QDRANT_URL=http://localhost:6333
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

3.  **Start Infrastructure**:
    Run Docker Compose to start MinIO and Qdrant.
    ```bash
    docker-compose up -d
    ```

4.  **Backend Setup**:
    Navigate to the `backend/app` directory (or root) and install dependencies.
    ```bash
    pip install -r backend/app/requirements.txt
    ```

5.  **Frontend Setup**:
    Navigate to the `frontend` directory.
    ```bash
    cd frontend
    npm install
    ```

## Usage

### 1. Ingestion
Before querying, you need to ingest documents.
1.  Upload PDF documents to your MinIO bucket (`insurance-docs`).
2.  Run the ingestion script:
    ```bash
    python -m app.ingestion.scripts.pipeline
    ```
    (Make sure you are running this from the `backend` directory so the module resolution works, e.g., `python -m app.ingestion.scripts.pipeline`)

### 2. Running the Backend API
Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`. Swagger UI is available at `http://localhost:8000/docs`.

### 3. Running the Frontend
Start the React development server:
```bash
cd frontend
npm run dev
```

## Project Structure

-   `backend/app/`: Contains the FastAPI application code.
    -   `ingestion/`: Scripts for processing PDFs and storing embeddings.
    -   `retrieval/`: Logic for querying Qdrant and reranking results.
    -   `llm/`: Interface with Google Gemini for answer generation.
    -   `utils/`: Utility functions (caching, etc.).
-   `frontend/`: React-based frontend application.
