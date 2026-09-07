# Deployment

## Architecture

The application uses a managed Neon PostgreSQL database with the
pgvector extension and Google's Gemini API.

```text
                         Internet
                            |
                            v
                    FastAPI Application
                            |
              +-------------+-------------+
              |                           |
              v                           v
        Gemini API                  Neon PostgreSQL
                                      |
                                      v
                                   pgvector
'''
