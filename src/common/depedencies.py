from fastapi import HTTPException, Header, status

from src.common.basemodel import User, UserRole
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
		user = await get_current_user(token=authorization)
		if user.role != self._role:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Forbidden, you don't have permission to access this resource.",
			)

		return user
