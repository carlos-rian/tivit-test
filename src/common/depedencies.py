from fastapi import HTTPException, Header, status

from src.common.basemodel import User, UserRole
from src.common.logger import Logger
from src.common.oauth import get_current_user


class Authentication:
	def __init__(self, role: UserRole):
		self._role = role

	async def authorization(
		self,
		authorization: str = Header(
			...,
			alias="Authorization",
			description="The authorization token is used to validate your identity on TIVIT.",
		),
	) -> User:
		Logger.debug(f"Checking authorization for: {self._role}")
		user = await get_current_user(token=authorization)

		if user.role != self._role:
			Logger.warning(f"User {user.username} is not allowed to access this resource.")
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Forbidden, you don't have permission to access this resource.",
			)
		Logger.info(f"User {user.username} is allowed to access this resource.")
		return user
