# RAGForge

A production-style AI knowledge platform built with **FastAPI, PostgreSQL, pgvector, Google Gemini, and Retrieval-Augmented Generation (RAG)**.

RAGForge allows users to upload documents, process and embed their content, perform semantic search, and interact with an LLM using retrieved document context. It also includes conversational chat, internal LLM tool calling, structured logging, health checks, testing, Docker support, and cloud deployment readiness.

---

## 🧠 Architecture

```text
                    User
                      |
                      v
                FastAPI API
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Document Pipeline          Chat / Agent
          |                       |
          v                       v
    Text Extraction          Google Gemini
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
    Google Gemini
          |
          v
     RAG Answer
```

### Agent / Tool Calling

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
Tool Results
 |
 v
Google Gemini
 |
 v
Final Answer
```

---

## ✨ Features

* FastAPI REST API
* PostgreSQL database
* pgvector semantic search
* SQLAlchemy ORM
* PDF, DOCX and TXT document ingestion
* Automatic text extraction
* Configurable text chunking
* 384-dimensional embeddings
* Sentence Transformers embedding model
* Retrieval-Augmented Generation
* Google Gemini LLM integration
* Conversational chat sessions
* Conversation history
* Internal LLM tool calling
* Document search tool
* Conversation history tool
* Structured application logging
* Database health checks
* LLM health checks
* Pytest test suite
* Docker support
* Neon PostgreSQL support
* Render deployment support

---

# 🔄 RAG Pipeline

```text
Upload Document
       |
       v
Extract Text
       |
       v
Create Chunks
       |
       v
Generate Embeddings
       |
       v
Store Embeddings
       |
       v
Neon PostgreSQL + pgvector
       |
       v
Semantic Vector Search
       |
       v
Retrieve Relevant Chunks
       |
       v
Build RAG Context
       |
       v
Google Gemini
       |
       v
Answer with Retrieved Sources
```

The application uses `all-MiniLM-L6-v2` by default for generating 384-dimensional embeddings.

---

# 🤖 LLM

RAGForge uses **Google Gemini** for:

* RAG question answering
* Conversational chat
* Agent/tool calling
* LLM health checks

The LLM configuration is controlled through environment variables.

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_gemini_model
```

The application does **not** depend on Ollama in the current architecture.

---

# 🗄️ Database

RAGForge uses:

**PostgreSQL + pgvector**

For cloud deployment, the recommended database is:

**Neon PostgreSQL**

The database stores:

* Documents
* Document chunks
* Embeddings
* Chat sessions
* Chat messages

Vector similarity search is handled using PostgreSQL's `pgvector` extension.

---

# 🌐 Production Architecture

The intended deployment architecture is:

```text
                         Internet
                            |
                            v
                     Render Web Service
                            |
                            v
                      RAGForge API
                       FastAPI
                            |
              +-------------+-------------+
              |                           |
              v                           v
       Neon PostgreSQL              Google Gemini
          + pgvector                    API
              |
              v
        Document Data
        Vector Embeddings
        Chat History
```

### Services

| Component        | Technology            |
| ---------------- | --------------------- |
| API              | FastAPI               |
| Language         | Python                |
| LLM              | Google Gemini         |
| Embeddings       | Sentence Transformers |
| Vector Database  | PostgreSQL + pgvector |
| Cloud Database   | Neon                  |
| Hosting          | Render                |
| ORM              | SQLAlchemy            |
| Testing          | Pytest                |
| Containerization | Docker                |

---

# 🚀 API

## Root

```text
GET /
```

## Health

```text
GET /health/
GET /health/database
GET /health/llm
```

## Documents

```text
POST /documents/upload

GET /documents/

GET /documents/{document_id}

POST /documents/{document_id}/process

GET /documents/{document_id}/chunks

DELETE /documents/{document_id}
```

## Search

```text
POST /search/
```

## Chat

```text
POST /chat/sessions

GET /chat/sessions

GET /chat/sessions/{session_id}

POST /chat/sessions/{session_id}/ask

GET /chat/sessions/{session_id}/messages
```

## Agent

```text
POST /agent/
```

The agent can use internal tools for:

```text
search_documents()
get_conversation_history()
```

---

# 📁 Project Structure

```text
ragforge/
│
├── app/
│   ├── agents/
│   │   ├── agent.py
│   │   └── tools.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging_config.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   └── session.py
│   │
│   ├── routers/
│   │   ├── agent.py
│   │   ├── chat.py
│   │   ├── documents.py
│   │   ├── health.py
│   │   └── search.py
│   │
│   ├── schemas/
│   │   ├── agent.py
│   │   ├── chat.py
│   │   ├── chunk.py
│   │   ├── document.py
│   │   └── search.py
│   │
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── chunking_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── processing_service.py
│   │   └── search_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_agent.py
│   ├── test_chat.py
│   ├── test_chunking.py
│   ├── test_documents.py
│   ├── test_health.py
│   └── test_search.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
├── DEPLOYMENT.md
└── README.md
```

---

# ⚙️ Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/BELBINBENORM/ragforge.git

cd ragforge
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file:

```text
DATABASE_URL=your_neon_postgresql_connection_string

GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=your_gemini_model

EMBEDDING_MODEL=all-MiniLM-L6-v2

UPLOAD_DIR=data/documents

CHUNK_SIZE=1000

CHUNK_OVERLAP=200

TOP_K=5

SIMILARITY_THRESHOLD=0.35

MAX_FILE_SIZE_MB=20

MAX_CHAT_HISTORY=10
```

Never commit `.env` to Git.

---

# 🗃️ Database Initialization

After configuring the database:

```bash
python -m app.database.init_db
```

This initializes the required PostgreSQL tables and enables the `vector` extension.

For Neon, the database must support the `pgvector` extension.

---

# ▶️ Run Locally

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Testing

Run the complete test suite:

```bash
pytest -v
```

Tests cover:

* Document operations
* Text chunking
* Semantic search
* Chat functionality
* Health endpoints
* Agent request validation

---

# 📝 Logging

Application logs are written to:

```text
logs/app.log
```

The API records:

* Request method
* Request path
* Response status
* Request duration
* Application events

Sensitive information such as API keys, passwords and database credentials must never be logged.

---

# 🐳 Docker

RAGForge includes Docker support for local development and deployment.

Build the image:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

The application image is:

```text
ragforge:latest
```

The API container is:

```text
ragforge
```

The Compose project is configured as:

```text
ragforge
```

---

# ☁️ Deployment

RAGForge is designed for cloud deployment using:

```text
Render
   |
   v
RAGForge FastAPI
   |
   +---- Neon PostgreSQL + pgvector
   |
   +---- Google Gemini API
```

### Render

The FastAPI application can be deployed as a Render Web Service using the included `Dockerfile`.

The application listens on:

```text
0.0.0.0:8000
```

The production deployment should use the `PORT` provided by the hosting platform if required by the deployment configuration.

### Neon

Neon provides the managed PostgreSQL database used by the production deployment.

The `DATABASE_URL` environment variable should contain the Neon connection string.

### Google Gemini

The Gemini API is accessed through the configured:

```text
GEMINI_API_KEY
```

and:

```text
GEMINI_MODEL
```

---

# ❤️ Health Checks

RAGForge provides dedicated endpoints for deployment monitoring.

### API

```text
GET /health/
```

### Database

```text
GET /health/database
```

### Gemini

```text
GET /health/llm
```

These endpoints can be used to verify the application's API, database and LLM dependencies.

---

# 🔒 Production Considerations

For production deployment:

* Store secrets using Render environment variables
* Use Neon for managed PostgreSQL
* Enable pgvector in the database
* Never commit `.env`
* Never expose database credentials
* Use HTTPS
* Configure persistent document storage
* Monitor application logs
* Configure health checks
* Restrict uploaded file sizes
* Avoid logging sensitive values
* Use production-grade environment configuration

---

# 🧩 MCP

MCP is **not implemented in the current version**.

RAGForge currently uses an internal tool-calling architecture where the LLM can invoke application-level tools such as:

```text
search_documents()
get_conversation_history()
```

This provides a foundation for exploring MCP separately without unnecessarily coupling the current RAG backend to the protocol.

---

# 🎯 Why There Is No ML Prediction Endpoint

RAGForge is intentionally focused on:

```text
Document Intelligence
        +
Semantic Search
        +
RAG
        +
LLM Applications
```

Traditional ML prediction, TensorFlow projects, model training and predictive modeling belong to separate projects in the overall AI/ML portfolio.

Adding an unrelated prediction endpoint would make this application less coherent.

---

# 🔄 End-to-End Flow

```text
User
 |
 v
Upload Document
 |
 v
Extract Text
 |
 v
Chunk Document
 |
 v
Generate Embeddings
 |
 v
Store in Neon PostgreSQL
 |
 v
User asks a question
 |
 v
Generate Query Embedding
 |
 v
Vector Similarity Search
 |
 v
Retrieve Relevant Chunks
 |
 v
Build RAG Prompt
 |
 v
Google Gemini
 |
 v
Generate Answer
 |
 v
Return Answer + Retrieved Sources
```

---

# 🛠️ Technology Stack

```text
Python
FastAPI
PostgreSQL
pgvector
SQLAlchemy
Google Gemini
Sentence Transformers
PyMuPDF
python-docx
Pytest
Docker
Neon
Render
```

---

# 📌 Project

**RAGForge**

AI-powered document knowledge platform combining semantic search, RAG, conversational AI and LLM tool calling into a production-style FastAPI backend.

**GitHub:** https://github.com/BELBINBENORM/ragforge

**Live API:** [ADD RENDER DEPLOYMENT LINK HERE]

