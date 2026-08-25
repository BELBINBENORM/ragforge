def test_agent_validation(client):
    response = client.post(
        "/agent/",
        json={"question": ""},
    )
    assert response.status_code == 422
