import os


os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

os.environ["USE_MOCK_AI"] = "true"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_register_login():

    email = "test@example.com"


    response = client.post(
        "/api/auth/register",
        json={
            "name": "Tester",
            "email": email,
            "password": "secret123"
        }
    )


    assert response.status_code in (
        200,
        409
    )


    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "secret123"
        }
    )


    assert response.status_code == 200


    response = client.get(
        "/api/auth/session"
    )


    assert response.status_code == 200


def test_home_requires_auth():

    unauthenticated_client = (
        TestClient(app)
    )


    response = (
        unauthenticated_client
        .post(
            "/api/recommendations/home",
            json={
                "budget": 50000,
                "room": "Bedroom",
                "style": "Modern",
                "items": [
                    {
                        "category": "Light",
                        "quantity": 2,
                        "notes": ""
                    }
                ]
            }
        )
    )


    assert response.status_code == 401