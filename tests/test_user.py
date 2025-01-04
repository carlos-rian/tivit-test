from starlette.testclient import TestClient

from src.common.oauth import create_access_token
from src.schema.user import GetAdminOut, GetUserOut


def test_get_admin_200(client: TestClient, a_token: str):
	response = client.get("/fake/admin", headers={"Authorization": a_token})
	assert response.status_code == 200
	data = response.json()

	assert GetAdminOut.model_validate(data) == GetAdminOut()


def test_get_user_200(client: TestClient, u_token: str):
	response = client.get("/fake/user", headers={"Authorization": u_token})
	assert response.status_code == 200
	data = response.json()

	assert GetUserOut.model_validate(data) == GetUserOut()


def test_get_user_401_invalid_token(client: TestClient, a_token: str):
	response = client.get("/fake/user", headers={"Authorization": a_token})
	assert response.status_code == 403
	data = response.json()
	assert data["detail"] == "Forbidden, you don't have permission to access this resource."


def test_get_admin_401_invalid_token(client: TestClient, u_token: str):
	response = client.get("/fake/admin", headers={"Authorization": u_token})
	assert response.status_code == 403
	data = response.json()
	assert data["detail"] == "Forbidden, you don't have permission to access this resource."


def test_get_user_422_no_token(client: TestClient):
	response = client.get("/fake/user")
	assert response.status_code == 422
	data = response.json()
	assert data == {
		"detail": [{"input": None, "loc": ["header", "Authorization"], "msg": "Field required", "type": "missing"}]
	}


def test_get_admin_422_no_token(client: TestClient):
	response = client.get("/fake/admin")
	assert response.status_code == 422
	data = response.json()
	assert data == {
		"detail": [{"input": None, "loc": ["header", "Authorization"], "msg": "Field required", "type": "missing"}]
	}


def test_get_user_401_bad_token(client: TestClient):
	response = client.get("/fake/user", headers={"Authorization": "Bearer invalid_token"})
	assert response.status_code == 401
	data = response.json()
	assert data == {"detail": "Invalid credentials"}


def test_get_admin_401_bad_token(client: TestClient):
	response = client.get("/fake/admin", headers={"Authorization": "Bearer invalid_token"})
	assert response.status_code == 401
	data = response.json()
	assert data == {"detail": "Invalid credentials"}


def test_get_user_401_token_without_sub(client: TestClient):
	u_token = create_access_token(data={"role": "admin"})["access_token"]
	response = client.get("/fake/user", headers={"Authorization": u_token})
	assert response.status_code == 401
	data = response.json()
	assert data == {"detail": "Invalid credentials"}


def test_get_user_401_sub_does_not_exist(client: TestClient):
	u_token = create_access_token(data={"sub": "invalid_user", "role": "admin"})["access_token"]
	response = client.get("/fake/user", headers={"Authorization": u_token})
	assert response.status_code == 401
	data = response.json()
	assert data == {"detail": "Invalid credentials"}
