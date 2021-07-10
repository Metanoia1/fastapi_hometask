import pytest

from fastapi.testclient import TestClient

from main import create_app



@pytest.fixture(scope="session")
def client() -> TestClient:
    app = create_app()
    return TestClient(app)



class TestCreateUser:
    def test_create_user(self, client: TestClient):
        data = {"username": "test", "email": "email@example.com"}

        response = client.post("/users/", json=data)

        assert response.status_code == 201
        response_data = response.json()
        assert response_data["username"] == "test"
        assert response_data["email"] == "email@example.com"
        assert "id" in response_data

    def test_create_user_fails(self, client: TestClient):
        data = {"username": "test", "email": "not_a_valid_email"}

        response = client.post("/users/", json=data)

        assert response.status_code == 422
