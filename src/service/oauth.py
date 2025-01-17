from fastapi import HTTPException, status

from src.common.logger import Logger
from src.common.oauth import create_access_token, verify_password
from src.database.oauth import OAuthDB
from src.schema.oauth import PostTokenIn, PostTokenOut


class OAuthService:
	@staticmethod
	async def post_token(data: PostTokenIn) -> PostTokenOut:
		Logger.info(f"Attempting to authenticate user: {data.username}")
		user = await OAuthDB.select_user_by_username(username=data.username)

		if user is None or verify_password(plain_password=data.password, hashed_password=user.password) is False:
			Logger.warning(f"Failed to authenticate user: {data.username}")
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

		Logger.info(f"User authenticated, generating token for: {data.username}")
		token_info = create_access_token(data={"sub": user.username, "role": user.role.value})
		return PostTokenOut.model_validate(token_info)
