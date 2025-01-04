from starlette.testclient import TestClient


def test_get_scalar_200(client: TestClient):
	response = client.get("/scalar")
	assert response.status_code == 200


def test_get_swagger_200(client: TestClient):
	response = client.get("/docs")
	assert response.status_code == 200


def test_get_redoc_200(client: TestClient):
	response = client.get("/redoc")
	assert response.status_code == 200


def test_get_openapi_200(client: TestClient):
	response = client.get("/openapi.json")
	assert response.status_code == 200
