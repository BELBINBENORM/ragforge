def test_invalid_search_query(client):

    response = client.post(
        "/search/",
        json={
            "query": "",
            "top_k": 5,
        },
    )

    assert response.status_code == 422


def test_invalid_top_k(client):

    response = client.post(
        "/search/",
        json={
            "query": "python",
            "top_k": 50,
        },
    )

    assert response.status_code == 422