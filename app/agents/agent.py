import json
import logging

import ollama
from sqlalchemy.orm import Session

from app.config import settings
from app.agents.tools import search_documents, get_conversation_history

logger = logging.getLogger(__name__)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search the document knowledge base using semantic vector search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_conversation_history",
            "description": "Get previous messages from a chat session.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {"type": "integer"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 20},
                },
                "required": ["session_id"],
            },
        },
    },
]


def run_agent(
    db: Session,
    question: str,
    session_id: int | None = None,
):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant for a document knowledge platform. "
                "Use tools when document retrieval or conversation history is needed. "
                "Do not invent information."
            ),
        },
        {"role": "user", "content": question},
    ]

    if session_id is not None:
        # Give the model a hint that history is available without
        # automatically fetching it on every request.
        messages[0]["content"] += (
            f" The current chat session id is {session_id}; "
            "use get_conversation_history if prior messages matter."
        )

    for _ in range(5):
        response = ollama.chat(
            model=settings.ollama_model,
            messages=messages,
            tools=TOOLS,
        )

        message = response["message"]
        tool_calls = message.get("tool_calls") or []

        if not tool_calls:
            return message["content"].strip()

        messages.append(message)

        for call in tool_calls:
            name = call["function"]["name"]
            arguments = call["function"].get("arguments", {})

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            if name == "search_documents":
                result = search_documents(
                    db=db,
                    query=arguments["query"],
                    top_k=arguments.get("top_k", 5),
                )
            elif name == "get_conversation_history":
                result = get_conversation_history(
                    db=db,
                    session_id=arguments["session_id"],
                    limit=arguments.get("limit", 10),
                )
            else:
                result = {"error": f"Unknown tool: {name}"}

            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result, default=str),
                }
            )

    raise RuntimeError("Agent exceeded maximum tool-call iterations.")
