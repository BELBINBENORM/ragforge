from pathlib import Path

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    document = pymupdf.open(path)

    try:

        text_parts = []

        for page in document:

            page_text = page.get_text()

            if page_text.strip():
                text_parts.append(page_text)

        return "\n".join(text_parts)

    finally:
        document.close()


def extract_text_from_docx(file_path: str) -> str:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    document = Document(path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def extract_text(
    file_path: str,
    file_type: str,
) -> str:

    file_type = file_type.lower().lstrip(".")

    if file_type == "pdf":
        return extract_text_from_pdf(file_path)

    if file_type == "docx":
        return extract_text_from_docx(file_path)

    if file_type == "txt":
        return extract_text_from_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {file_type}"
    )