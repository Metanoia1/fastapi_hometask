from fastapi.testclient import TestClient


class TestListPost:
    def test_list_post(self, client: TestClient):
        response = client.get("/posts/")
        assert response.status_code == 200
        response_data = response.json()[0]
        assert "id" in response_data
        assert "title" in response_data
        assert "body" in response_data
        assert "author" in response_data


class TestCreatePost:
    def test_create_post(self, client: TestClient):
        data = {"author_id": 1, "title": "asdf", "body": "qwer"}
        response = client.post("/posts/", json=data)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["author_id"] == 1
        assert response_data["title"] == "asdf"
        assert response_data["body"] == "qwer"
        assert "id" in response_data

    def test_create_post_fails(self, client: TestClient):
        data = {"author_id": "aasdf", "title": 1, "body": "qwer"}
        response = client.post("/posts/", json=data)
        assert response.status_code == 422


class TestDetailPost:
    def test_detail_post(self, client: TestClient):
        response = client.get("/posts/1")
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert "title" in response_data
        assert "body" in response_data
        assert "author" in response_data
        assert "comments" in response_data


class TestUpdatePost:
    def test_update_post(self, client: TestClient):
        data = {"title": "asdf", "body": "qwer"}
        response = client.put("/posts/1", json=data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == "asdf"
        assert response_data["body"] == "qwer"
        assert "id" in response_data

    def test_update_post_fails(self, client: TestClient):
        data = {"titl": "asdf", "body": "qwer"}
        response = client.post("/posts/1", json=data)
        assert response.status_code == 405
        response = client.put("/posts/1", json=data)
        assert response.status_code == 422
