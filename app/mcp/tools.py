from mcp.server.mcpserver import MCPServer

from app.database.session import get_db_session
from app.services.chat_service import get_chat_messages
from app.services.search_service import search_similar_chunks


def register_search_tool(mcp: MCPServer):
    @mcp.tool(
        name="search_documents",
        description="Search for similar chunks in the database using semantic vector search."
    )
    def search_documents(
        query: str,
        top_k: int = 5,
    ):
        top_k = min(max(top_k,1), 20)  # Ensure top_k is between 1 and 20
        db_session = get_db_session()
        try:
            results = search_similar_chunks(
                db=db_session, 
                query=query, 
                top_k=top_k)
            return [
                {
                   "document_id": r["document_id"],
                    "document_title": r["document_title"],
                    "chunk_index": r["chunk_index"],
                    "content": r["content"],
                    "similarity": r["similarity"], 
                }
                for r in results
            ]
        finally:
            db_session.close()

def register_conversation_tool(mcp: MCPServer):
    @mcp.tool(
        name="get_conversation_history",
        description="Retrieve the conversation history with the AI model, Chat session, or user interactions."
    )
    def get_conversation_history(
        session_id: int,
        limit: int = 10,
    ):
        limit = min(max(limit,1), 20)  # Ensure limit is between 1 and 20
        db_session = get_db_session()
        try:
            
            history = get_chat_messages(
                db=db_session, 
                session_id=session_id, 
                limit=limit)
            return[
                {
                    "role": h["role"],
                    "content": h["content"],
                }
                for h in history
            ]
        finally:
            db_session.close()