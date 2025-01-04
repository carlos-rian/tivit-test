import pytest

from src.common.basedb import DatabasePool
from src.common.helper import initialize_users


@pytest.mark.asyncio
async def test_database_initialize_users(client):
	assert await initialize_users(pool=DatabasePool) is None
