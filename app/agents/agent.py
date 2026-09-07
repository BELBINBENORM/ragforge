import logging

from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.config import settings
from app.agents.tools import (
    search_documents,
    get_conversation_history,
)

logger = logging.getLogger(__name__)


client = genai.Client(
    api_key=settings.gemini_api_key
)


SYSTEM_PROMPT = """
You are an AI assistant for a document-based knowledge
and question-answering system.

Use the available tools when document retrieval or
conversation history is needed.

Rules:

1. Use retrieved documents as the primary source of truth.
2. Do not invent information.
3. Do not make unsupported claims.
4. Use conversation history when it is relevant.
5. Keep answers clear and concise.
"""


TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_documents",
                description=(
                    "Search the document knowledge base "
                    "using semantic vector search."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "query": types.Schema(
                            type="STRING",
                            description="The search query.",
                        ),
                        "top_k": types.Schema(
                            type="INTEGER",
                            description="Number of results to return.",
                        ),
                    },
                    required=["query"],
                ),
            ),
            types.FunctionDeclaration(
                name="get_conversation_history",
                description=(
                    "Get previous messages from a chat session."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "session_id": types.Schema(
                            type="INTEGER",
                            description="The chat session ID.",
                        ),
                        "limit": types.Schema(
                            type="INTEGER",
                            description="Maximum number of messages.",
                        ),
                    },
                    required=["session_id"],
                ),
            ),
        ]
    )
]


def run_agent(
    db: Session,
    question: str,
    session_id: int | None = None,
):
    if session_id is not None:
        question = (
            f"{question}\n\n"
            f"The current chat session ID is {session_id}. "
            "Use get_conversation_history if previous "
            "messages are relevant."
        )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=question)
            ],
        )
    ]

    for _ in range(5):

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=TOOLS,
            ),
        )

        candidate = response.candidates[0]

        contents.append(candidate.content)

        function_calls = [
            part.function_call
            for part in candidate.content.parts
            if part.function_call
        ]

        # Gemini decided no tool is required
        if not function_calls:

            if response.text:
                return response.text.strip()

            return "I could not generate an answer."

        tool_results = []

        for function_call in function_calls:

            name = function_call.name

            arguments = dict(
                function_call.args or {}
            )

            if name == "search_documents":

                result = search_documents(
                    db=db,
                    query=arguments["query"],
                    top_k=min(
                        max(
                            arguments.get("top_k", 5),
                            1,
                        ),
                        10,
                    ),
                )

            elif name == "get_conversation_history":

                result = get_conversation_history(
                    db=db,
                    session_id=arguments["session_id"],
                    limit=min(
                        max(
                            arguments.get("limit", 10),
                            1,
                        ),
                        20,
                    ),
                )

            else:

                result = {
                    "error": f"Unknown tool: {name}"
                }

            tool_results.append(
                types.Part.from_function_response(
                    name=name,
                    response={
                        "result": result
                    },
                )
            )

        contents.append(
            types.Content(
                role="tool",
                parts=tool_results,
            )
        )

    raise RuntimeError(
        "Agent exceeded maximum tool-call iterations."
    )