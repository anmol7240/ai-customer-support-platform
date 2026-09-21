from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200


def test_db_health():
    response = client.get("/db-health")

    assert response.status_code == 200


def test_predict_category():
    response = client.post(
        "/predict-category",
        params={
            "message": "My payment was deducted"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "predicted_category" in data
    assert isinstance(
        data["predicted_category"],
        str
    )


def test_ticket_analytics():
    response = client.get("/analytics/tickets")

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200