# AI Knowledge Platform

A production-style FastAPI application for document ingestion, semantic search, Retrieval-Augmented Generation (RAG), LLM chat, and LLM tool calling.

The project focuses on turning a working RAG pipeline into a maintainable backend application with PostgreSQL, pgvector, testing, logging, Docker, and deployment readiness.

## Architecture

```text
Document
   |
   v
Text Extraction
   |
   v
Chunking
   |
   v
Sentence Transformer
   |
   v
PostgreSQL + pgvector
   |
   v
Vector Search
   |
   v
Retrieved Context
   |
   v
Ollama LLM
   |
   v
RAG Answer
```

Agent/tool calling extends the application:

```text
User
  |
  v
LLM Agent
  |
  +---- search_documents()
  |
  +---- get_conversation_history()
  |
  v
Tool Result
  |
  v
LLM
  |
  v
Final Answer
```

## Features

- PostgreSQL persistence
- SQLAlchemy ORM
- PDF, DOCX and TXT ingestion
- Text chunking
- 384-dimensional embeddings
- pgvector semantic search
- Retrieval-Augmented Generation
- Ollama LLM integration
- Chat sessions and history
- LLM agent/tool calling
- Structured application logging
- Health checks
- Pytest test suite
- Docker support
- Deployment documentation

## API

### Root

```text
GET /
```

### Health

```text
GET /health/
GET /health/database
GET /health/llm
```

### Documents

```text
POST /documents/upload
GET /documents/
GET /documents/{document_id}
POST /documents/{document_id}/process
GET /documents/{document_id}/chunks
DELETE /documents/{document_id}
```

### Search

```text
POST /search/
```

### Chat

```text
POST /chat/sessions
GET /chat/sessions
GET /chat/sessions/{session_id}
POST /chat/sessions/{session_id}/ask
GET /chat/sessions/{session_id}/messages
```

### Agent

```text
POST /agent/
```

The agent can use internal tools for document search and conversation history.

## Project structure

```text
app/
├── agents/
│   ├── agent.py
│   └── tools.py
│
├── core/
│   ├── config.py
│   └── logging_config.py
│
├── database/
│   ├── connection.py
│   ├── session.py
│   ├── models.py
│   └── init_db.py
│
├── routers/
│   ├── documents.py
│   ├── search.py
│   ├── chat.py
│   ├── health.py
│   └── agent.py
│
└── services/
    ├── document_service.py
    ├── extraction_service.py
    ├── chunking_service.py
    ├── embedding_service.py
    ├── vector_search_service.py
    ├── rag_service.py
    └── llm_service.py

tests/
├── conftest.py
├── test_chat.py
├── test_chunking.py
├── test_documents.py
├── test_health.py
├── test_search.py
└── test_agent.py
```

## Setup

Create and activate a virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```text
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/ai_knowledge
OLLAMA_MODEL=llama3.2
EMBEDDING_MODEL=all-MiniLM-L6-v2
UPLOAD_DIR=data/documents
```

Initialize the database:

```bash
python -m app.database.init_db
```

Make sure Ollama is running and the configured model is available.

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run the complete suite:

```bash
pytest -v
```

The tests cover the existing document, chunking, search, chat and health functionality, plus agent request validation.

## Logging

Application logs are written to:

```text
logs/app.log
```

The API also logs request method, path, status code and request duration.

Sensitive values such as passwords, tokens and API keys should never be logged.

## Docker

Build and start the application stack:

```bash
docker compose up --build
```

The local stack contains:

```text
FastAPI
PostgreSQL + pgvector
```

Ollama is intentionally kept outside the Compose stack for the current development setup because the LLM runtime is local.

See `DEPLOYMENT.md` for production deployment considerations.

## Why this project does not contain an ML prediction endpoint

This application is specifically an AI Knowledge Platform centered on document intelligence and RAG.

ML model training, tuning, TensorFlow and predictive modeling are separate areas of the overall AI Engineer portfolio. Adding an unrelated prediction model here would make the architecture less coherent rather than better.

## MCP

MCP is intentionally not implemented in this version.

The project first establishes a clean internal tool-calling architecture. MCP can be explored separately later if it becomes useful for exposing those tools to external AI clients.

## Current pipeline

```text
Upload document
      |
      v
Extract text
      |
      v
Create chunks
      |
      v
Generate embeddings
      |
      v
Store in PostgreSQL + pgvector
      |
      v
Semantic retrieval
      |
      v
Build RAG context
      |
      v
Ollama LLM
      |
      v
Answer with retrieved sources
```
