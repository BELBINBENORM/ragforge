def test_root(client):

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "AI Knowledge Platform API"
    )


def test_health(client):

    response = client.get(
        "/health/"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"