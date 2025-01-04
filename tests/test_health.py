from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.common.basedb import DatabasePool


@pytest.mark.asyncio
async def test_get_health_200(client: TestClient):
	with patch.object(DatabasePool.pool, "_opened", True):
		response = client.get("/fake/health")
		assert response.status_code == 200
		assert response.json() == {"status": "ok", "message": "API is healthy"}


@pytest.mark.asyncio
async def test_get_health_417(client: TestClient):
	with patch.object(DatabasePool.pool, "_opened", False):
		response = client.get("/fake/health")
		assert response.status_code == 417
		assert response.json() == {"status": "error", "message": "API is not healthy"}
