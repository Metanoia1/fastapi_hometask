from fastapi.testclient import TestClient


class TestCreateUser:
    def test_create_user(self, client: TestClient):
        data = {
            "name": "laskdj",
            "username": "test",
            "email": "email@example.com",
            "phone": "alskdjflasdkfj",
        }
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
