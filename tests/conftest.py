import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi.testclient import TestClient

from src.common.oauth import create_access_token
from src.main import create_app


@pytest_asyncio.fixture(scope="session", name="client")
async def app():
	"""create a test client for the app"""
	app = create_app()

	async with LifespanManager(app, 10, 10) as manager:
		yield TestClient(manager.app)


@pytest.fixture(scope="session", name="u_token")
def user_token():
	token = create_access_token(data={"sub": "user", "role": "user"})
	return token["access_token"]


@pytest.fixture(scope="session", name="a_token")
def admin_token():
	token = create_access_token(data={"sub": "admin", "role": "admin"})
	return token["access_token"]
