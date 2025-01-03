from datetime import datetime
from uuid import UUID

from src.common.basedb import DatabasePool
from src.common.basemodel import BaseModel, UserRole


class OAuthTB(BaseModel):
	id: UUID
	username: str
	password: str
	role: UserRole
	created_at: datetime
	updated_at: datetime


class OAuthDB:
	@staticmethod
	async def select_user_by_username(username: str):
		async with DatabasePool.pool.connection() as conn:
			return await conn.query_first(
				sql="SELECT * FROM OAuth2 WHERE username = :username",
				parameters={"username": username},
				model=OAuthTB,
			)
