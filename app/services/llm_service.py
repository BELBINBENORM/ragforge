from google import genai

from app.config import settings

import logging

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are an AI assistant for a document-based knowledge and
question-answering system.

Your job is to answer questions using the retrieved document
context provided to you.

Rules:

1. Use the retrieved documents as the primary source of truth.
2. Do not invent facts.
3. Do not make unsupported claims.
4. Use conversation history when resolving references such as
   "he", "she", "it", "that document", or "his skills".
5. If the answer is not supported by the retrieved context,
   say exactly:

"I could not find the answer in the provided documents."

6. Keep answers clear and concise.
"""


def build_prompt(
    question: str,
    context: str,
    chat_history: list[dict],
) -> str:

    history_text = "No previous conversation."

    if chat_history:

        history_parts = []

        for message in chat_history:

            role = message["role"].upper()
            content = message["content"]

            history_parts.append(
                f"{role}: {content}"
            )

        history_text = "\n".join(history_parts)

    return f"""
Previous conversation:

{history_text}
Retrieved document context:
{context}
Current question:
{question}
Answer:
"""

client = genai.Client(
    api_key=settings.gemini_api_key
)


def generate_answer(
    question: str,
    context: str,
    chat_history: list[dict] | None = None,
) -> str:

    if chat_history is None:
        chat_history = []

    prompt = build_prompt(
        question=question,
        context=context,
        chat_history=chat_history,
    )

    logger.info(
        "LLM request started using model=%s",
        settings.gemini_model,
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""
{SYSTEM_PROMPT}

{prompt}
"""
                    }
                ],
            }
        ],
    )

    answer = response.text.strip()

    logger.info("LLM response generated")

    return answer