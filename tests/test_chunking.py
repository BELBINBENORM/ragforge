from app.services.chunking_service import chunk_text


def test_chunk_text():

    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) > 1

    assert all(
        len(chunk) <= 1000
        for chunk in chunks
    )


def test_empty_text():

    assert chunk_text("") == []


def test_whitespace_text():

    assert chunk_text("   ") == []