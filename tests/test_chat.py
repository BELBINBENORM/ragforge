def test_create_chat_session(client):

    response = client.post(
        "/chat/sessions",
        json={
            "title": "Test Chat"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Chat"

    assert "id" in data


def test_create_default_chat_session(client):

    response = client.post(
        "/chat/sessions",
        json={}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Chat"