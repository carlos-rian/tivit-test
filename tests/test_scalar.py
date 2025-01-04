from starlette.testclient import TestClient


def test_get_scalar_doc_200(client: TestClient):
	response = client.get("/scalar")
	assert response.status_code == 200


def test_get_scalar_doc_200(client: TestClient):
	response = client.get("/scalar")
	assert response.status_code == 200