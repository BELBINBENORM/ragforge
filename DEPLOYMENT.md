# Deployment

## Current architecture

The application is designed to run as:

```text
                Internet
                   |
                   v
              FastAPI API
                   |
          +--------+--------+
          |                 |
          v                 v
 PostgreSQL + pgvector    Ollama
```

For development, PostgreSQL can run locally or through Docker, while Ollama runs on the host machine.

## Local Docker deployment

Start PostgreSQL and the API:

```bash
docker compose up --build
```

Initialize the database:

```bash
docker compose exec api python -m app.database.init_db
```

Open:

```text
http://localhost:8000/docs
```

## Production considerations

For a real public deployment:

- use a managed PostgreSQL service with pgvector support
- keep database credentials in environment variables
- do not expose PostgreSQL directly to the internet
- use HTTPS
- configure an application-level reverse proxy or platform ingress
- run the API with multiple workers when appropriate
- use a production LLM endpoint or separately hosted LLM runtime
- configure persistent storage for uploaded documents
- centralize logs in the deployment environment

## Environment variables

```text
DATABASE_URL
OLLAMA_MODEL
EMBEDDING_MODEL
UPLOAD_DIR
```

Never commit `.env`.

## Health checks

The API exposes health endpoints that can be used by a deployment platform:

```text
GET /health/
GET /health/database
GET /health/llm
```
