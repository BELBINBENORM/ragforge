# RAGForge

### Live RAG & Agent Pipeline with MCP

RAGForge is a production-style AI knowledge platform that combines **Retrieval-Augmented Generation (RAG), semantic vector search, conversational memory, LLM agents, and Model Context Protocol (MCP)** into a modular FastAPI backend.

The platform supports document ingestion, embedding generation, vector retrieval, persistent conversations, and agentic tool use through MCP.

---

## 🚀 Live API

**Swagger / OpenAPI Documentation**

https://ragforge-htnl.onrender.com/docs

> ⚠️ **Free Hosting Notice**
>
> RAGForge is deployed on Render's free tier. The service may spin down after inactivity. The first request can take some time while the service wakes up.

---

# 🧠 Architecture

RAGForge follows an **Agent → MCP Client → MCP Server → Tools → Services** architecture.

```text
                              ┌──────────────────────┐
                              │       Client         │
                              │      API / UI        │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │       FastAPI        │
                              │      REST API        │
                              └──────────┬───────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
             ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
             │  Documents  │     │   Search    │     │    Agent    │
             │   Router    │     │   Router    │     │   Router    │
             └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
                    │                   │                    │
                    ▼                   ▼                    ▼
             Document Service     Search Service       Agent Service
                                                           │
                                                           ▼
                                                    ┌─────────────┐
                                                    │   Gemini    │
                                                    │    Agent    │
                                                    └──────┬──────┘
                                                           │
                                                       MCP Client
                                                           │
                                                           ▼
                                                    ┌─────────────┐
                                                    │ MCP Server  │
                                                    └──────┬──────┘
                                                           │
                                      ┌────────────────────┴────────────────────┐
                                      │                                         │
                                      ▼                                         ▼
                              search_documents                    get_conversation_history
                                      │                                         │
                                      ▼                                         ▼
                                   pgvector                                 PostgreSQL
                                      │                                         │
                                      └────────────────────┬────────────────────┘
                                                           │
                                                           ▼
                                                    Tool Results
                                                           │
                                                           ▼
                                                    Gemini Agent
                                                           │
                                                           ▼
                                                    Final Response
```

---

# 🔄 Agentic RAG Flow

The main question-answering workflow is handled through the AI agent.

```text
User Question
      │
      ▼
POST /agent/run
      │
      ▼
Gemini Agent
      │
      ▼
MCP Client
      │
      ▼
MCP Server
      │
      ├──────────────► search_documents
      │                     │
      │                     ▼
      │               Query Embedding
      │                     │
      │                     ▼
      │                  pgvector
      │                     │
      │                     ▼
      │              Relevant Chunks
      │
      └──────────────► get_conversation_history
                            │
                            ▼
                       PostgreSQL
                            │
                            ▼
                     Chat History
                            │
                            ▼
                       Tool Results
                            │
                            ▼
                     Gemini Agent
                            │
                            ▼
                      Final Answer
                            │
                            ▼
                  Persist Conversation
```

The agent can dynamically determine which MCP tools are required and execute them before generating the final response.

---

# 🧩 MCP Layer

MCP provides the interface between the AI agent and application capabilities.

### MCP Client

The MCP client:

1. Connects to the MCP server.
2. Discovers available tools.
3. Retrieves tool definitions.
4. Provides tool definitions to Gemini.
5. Executes tool calls requested by the agent.
6. Returns tool results to the agent.

```text
MCP Client
    │
    ▼
list_tools()
    │
    ▼
Tool Definitions
    │
    ▼
Gemini Agent
    │
    ▼
call_tool()
    │
    ▼
MCP Server
```

---

# 🛠️ MCP Tools

## `search_documents`

Performs semantic document retrieval using embeddings and PostgreSQL `pgvector`.

```text
User Query
    │
    ▼
Embedding Model
    │
    ▼
Query Vector
    │
    ▼
pgvector Similarity Search
    │
    ▼
Relevant Chunks
```

## `get_conversation_history`

Retrieves previous messages for a conversation session from PostgreSQL.

```text
Session ID
    │
    ▼
PostgreSQL
    │
    ▼
Conversation History
```

---

# 📚 Document Ingestion Pipeline

Documents are transformed into searchable knowledge through the following pipeline:

```text
Document Upload
      │
      ▼
Text Extraction
      │
      ├── PDF
      ├── DOCX
      └── TXT
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Sentence Transformers
      │
      ▼
PostgreSQL + pgvector
```

### Supported Formats

- PDF
- DOCX
- TXT

### Embedding Model

```text
all-MiniLM-L6-v2
```

---

# 🔎 Semantic Search

RAGForge uses PostgreSQL with `pgvector` for vector similarity search.

```text
Query
  │
  ▼
Embedding Model
  │
  ▼
Query Vector
  │
  ▼
pgvector
  │
  ▼
Similarity Ranking
  │
  ▼
Top-K Relevant Chunks
```

Retrieval behavior can be configured using:

- `TOP_K`
- `SIMILARITY_THRESHOLD`

---

# 🤖 AI Agent

Google Gemini powers the agent layer.

The agent is responsible for:

- Understanding user requests
- Discovering available MCP tools
- Deciding when tools are required
- Executing MCP tools
- Processing retrieved context
- Using conversation history
- Generating the final response

The agent follows a tool-use loop:

```text
Question
   │
   ▼
Reason
   │
   ├── No tool required ───────► Answer
   │
   └── Tool required
          │
          ▼
       MCP Tool
          │
          ▼
      Tool Result
          │
          ▼
       Reason Again
          │
          ▼
        Answer
```

---

# 💬 Conversational Memory

RAGForge maintains persistent conversation sessions using PostgreSQL.

```text
Chat Session
     │
     ├── User Message
     │
     ├── Assistant Message
     │
     ├── User Message
     │
     └── Assistant Message
```

The agent can access previous messages through:

```text
get_conversation_history()
```

This allows contextual follow-up questions across multiple turns.

---

# 🗄️ Database Architecture

RAGForge uses **PostgreSQL + pgvector**.

The database stores:

- Documents
- Document chunks
- Embeddings
- Chat sessions
- Chat messages

SQLAlchemy provides the database abstraction layer.

```text
                    PostgreSQL
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
       Document Data          Chat Data
             │                     │
             ▼                     ▼
          pgvector            Sessions
          Embeddings          Messages
```

---

# 🌐 Deployment Architecture

```text
                         Internet
                            │
                            ▼
                     ┌─────────────┐
                     │   Render    │
                     │ Web Service │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  RAGForge   │
                     │   FastAPI   │
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        PostgreSQL       Gemini API     MCP Layer
        + pgvector
```

### Deployment Stack

| Component | Technology |
|---|---|
| API | FastAPI |
| Language | Python |
| LLM | Google Gemini |
| Agent | Gemini Agent |
| Protocol | Model Context Protocol |
| MCP | MCP Client + MCP Server |
| RAG | Retrieval-Augmented Generation |
| Embeddings | Sentence Transformers |
| Vector Database | PostgreSQL + pgvector |
| ORM | SQLAlchemy |
| Database Hosting | Neon PostgreSQL |
| Application Hosting | Render |
| Containerization | Docker |
| Testing | Pytest |

---

# 📡 API Endpoints

## Health

```http
GET /health/
GET /health/database
GET /health/llm
```

Used to verify application, database and LLM availability.

---

## Documents

```http
POST /documents/upload

GET /documents/

GET /documents/{document_id}

POST /documents/{document_id}/process

GET /documents/{document_id}/chunks

DELETE /documents/{document_id}
```

Handles document upload, processing, retrieval and deletion.

---

## Search

```http
POST /search/
```

Provides direct semantic search over indexed documents.

---

## Chat Sessions

```http
POST /chat/sessions

GET /chat/sessions

GET /chat/sessions/{session_id}

PATCH /chat/sessions/{session_id}

DELETE /chat/sessions/{session_id}

GET /chat/sessions/{session_id}/messages
```

Handles persistent chat sessions and conversation history.

---

## Agent

```http
POST /agent/run
```

Main agentic question-answering endpoint.

Example:

```json
{
  "question": "What skills are mentioned in my resume?",
  "session_id": 1
}
```

The agent can dynamically invoke MCP tools when additional context is required.

---

# 📁 Project Structure

```text
ragforge/
│
├── app/
│   │
│   ├── agents/
│   │   └── agent.py
│   │
│   ├── core/
│   │   └── logging_config.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   └── session.py
│   │
│   ├── mcp/
│   │   ├── client.py
│   │   ├── server.py
│   │   └── tools.py
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

## 1. Clone

```bash
git clone https://github.com/BELBINBENORM/ragforge.git

cd ragforge
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file using `.env.example`.

```env
DATABASE_URL=your_postgresql_connection_string

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

Never commit `.env` files or API keys to source control.

---

# 🗃️ Database Setup

Initialize the database:

```bash
python -m app.database.init_db
```

PostgreSQL must have the `pgvector` extension available.

---

# ▶️ Run Locally

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🐳 Docker

Build the application:

```bash
docker compose build
```

Start the services:

```bash
docker compose up
```

API:

```text
http://localhost:8000
```

---

# 🧪 Testing

Run the test suite:

```bash
pytest -v
```

Tests cover:

- Agent functionality
- Chat operations
- Document operations
- Text chunking
- Semantic search
- Health endpoints
- Request validation

---

# 📝 Logging

RAGForge includes application-level logging and HTTP request middleware.

The system records:

- HTTP method
- Request path
- Response status
- Request duration
- Application events
- Exceptions

Sensitive credentials should never be written to logs.

---

# 🏗️ Design Principles

### Separation of Concerns

```text
Routers
   │
   ▼
Services
   │
   ▼
Database / External APIs
```

Each layer has a defined responsibility.

### MCP Tool Abstraction

The agent interacts with application capabilities through MCP instead of depending directly on internal service implementations.

### Reusable Services

Core capabilities such as:

- Document processing
- Chunking
- Embedding generation
- Semantic search
- Chat persistence

are implemented as independent services.

### Configuration Driven

Core behavior is controlled through environment variables rather than hard-coded values.

---

# 🔁 Complete System

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                       POST /agent/run
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Gemini Agent     │
                    └──────────┬──────────┘
                               │
                          MCP Client
                               │
                               ▼
                    ┌─────────────────────┐
                    │     MCP Server      │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        search_documents          get_conversation_history
                 │                           │
                 ▼                           ▼
             pgvector                  PostgreSQL
                 │                           │
                 └─────────────┬─────────────┘
                               │
                               ▼
                         Tool Results
                               │
                               ▼
                         Gemini Agent
                               │
                               ▼
                         Final Answer
                               │
                               ▼
                       Chat Persistence
```

---

# 🎯 Key Features

- Document ingestion pipeline
- PDF, DOCX and TXT support
- Text chunking
- Sentence Transformer embeddings
- PostgreSQL vector search
- pgvector similarity retrieval
- Retrieval-Augmented Generation
- Gemini-powered AI agent
- MCP client and MCP server
- Dynamic MCP tool discovery
- MCP tool invocation
- Conversation memory
- Persistent chat sessions
- FastAPI REST API
- Swagger / OpenAPI documentation
- Docker support
- Database health checks
- LLM health checks
- Application logging
- Pytest test suite
- Environment-based configuration
- Cloud deployment

---

# 🛠️ Technology Stack

```text
Python
│
├── FastAPI
├── Pydantic
├── SQLAlchemy
│
├── Google Gemini
│
├── Model Context Protocol
│   ├── MCP Client
│   └── MCP Server
│
├── Sentence Transformers
│
├── PostgreSQL
│   └── pgvector
│
├── PyMuPDF
├── python-docx
│
├── Pytest
│
└── Docker
```

---

# 📌 Project Status

**Status:** Deployed

**Architecture:** Agentic RAG + MCP

**API:** FastAPI

**LLM:** Google Gemini

**Vector Search:** PostgreSQL + pgvector

**Embeddings:** Sentence Transformers

**Deployment:** Render + Neon PostgreSQL

---

# 🔗 Links

### GitHub

https://github.com/BELBINBENORM/ragforge

### Live API

https://ragforge-htnl.onrender.com/docs

---

## 👨‍💻 RAGForge

**Live RAG & Agent Pipeline with MCP**

A production-style AI knowledge platform demonstrating how **RAG, vector databases, conversational memory, LLM agents, MCP tools, FastAPI, PostgreSQL and Docker** can be combined into a modular AI backend.
