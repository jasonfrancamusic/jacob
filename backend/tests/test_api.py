from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "jacob-core-api"


def test_chat_morning_briefing():
    response = client.post(
        "/chat",
        json={"partner_name": "Jason", "message": "Bom dia, Jacob."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "morning_briefing"
    assert payload["specialist_name"] == "Morning Briefing Specialist"
    assert "Bom dia, Jason" in payload["text"]
    assert payload["reflection"]["helped"] is True


def test_chat_life_analytics():
    response = client.post(
        "/chat",
        json={"partner_name": "Jason", "message": "Como está minha vida em métricas?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "life_analytics"
    assert "Mapa da Vida" in payload["text"]


def test_chat_rejects_empty_message():
    response = client.post(
        "/chat",
        json={"partner_name": "Jason", "message": ""},
    )

    assert response.status_code == 422
