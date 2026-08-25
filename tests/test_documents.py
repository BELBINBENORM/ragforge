def test_invalid_document_type(client):

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.exe",
                b"fake content",
                "application/octet-stream",
            )
        },
    )

    assert response.status_code == 400


def test_empty_document(client):

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "empty.txt",
                b"",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400