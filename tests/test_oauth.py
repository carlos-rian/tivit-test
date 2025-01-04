from datetime import datetime

from starlette.testclient import TestClient


def test_post_token_201_admin(client: TestClient):
	response = client.post("/fake/token", params={"username": "admin", "password": "JKSipm0YH"})
	assert response.status_code == 201
	data = response.json()
	assert data["tokenType"] == "bearer"
	assert isinstance(data["accessToken"], str)
	assert isinstance(data["expiresIn"], int)
	assert isinstance(datetime.fromisoformat(data["expiresAt"]), datetime)


def test_post_token_201_user(client: TestClient):
	response = client.post("/fake/token", params={"username": "user", "password": "L0XuwPOdS5U"})
	assert response.status_code == 201
	data = response.json()
	assert data["tokenType"] == "bearer"
	assert isinstance(data["accessToken"], str)
	assert isinstance(data["expiresIn"], int)
	assert isinstance(datetime.fromisoformat(data["expiresAt"]), datetime)


def test_post_token_401_user(client: TestClient):
	response = client.post("/fake/token", params={"username": "user", "password": "uwPOdS5U"})
	assert response.status_code == 401
	data = response.json()
	assert data["detail"] == "Invalid username or password"
