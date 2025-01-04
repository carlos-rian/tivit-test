from uuid import uuid4

from src.common.basedb import DatabasePool
from src.common.basemodel import UserRole
from src.common.logger import Logger
from src.common.oauth import get_password_hash

TABLE = """
    CREATE TABLE IF NOT EXISTS OAuth2 (
        id          UUID            PRIMARY KEY,
        username    VARCHAR(255)    NOT NULL UNIQUE,
        password    VARCHAR(255)    NOT NULL,
        role        VARCHAR(255)    NOT NULL,
        created_at  TIMESTAMP       NOT NULL,
        updated_at  TIMESTAMP       NOT NULL
);"""

INSERT = """
    INSERT INTO OAuth2 (id, username, password, role, created_at, updated_at)
    VALUES (:id, :username, :password, :role, NOW(), NOW());
"""


async def initialize_users(pool: DatabasePool):
	Logger.debug("Initializing users...")
	async with pool.pool.connection() as conn:
		await conn.execute(TABLE)
		count_users = await conn.query_first(sql="SELECT COUNT(*) AS total FROM OAuth2")
		if count_users.total > 0:
			return

		users = [
			{"id": uuid4(), "username": "user", "role": UserRole.USER, "password": "L0XuwPOdS5U"},
			{"id": uuid4(), "username": "admin", "role": UserRole.ADMIN, "password": "JKSipm0YH"},
		]

		for user in users:
			user["password"] = get_password_hash(user["password"])
			await conn.execute(sql=INSERT, parameters=user)

	Logger.debug("Users initialized.")
