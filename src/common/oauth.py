# app/auth.py
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.common.basedb import DatabasePool
from src.common.basemodel import User
from src.main import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
	return pwd_context.verify(secret=plain_password, hash=hashed_password)


def get_password_hash(password: str) -> str:
	return pwd_context.hash(secret=password)


def create_access_token(data: dict) -> dict:
	to_encode = data.copy()
	expire = datetime.now(tz=UTC) + timedelta(minutes=Settings.JWT_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	return {
		"token_type": "bearer",
		"access_token": jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM),
		"expires_in": Settings.JWT_EXPIRE_MINUTES * 60,
		"expires_at": expire,
	}


async def get_user(username: str):
	async with DatabasePool.pool.connection() as conn:
		return await conn.query_first(
			sql="SELECT * FROM OAuth2 WHERE username = :username",
			parameters={"username": username},
			model=User,
		)


async def get_current_user(token: str):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Invalid credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)

	try:
		payload = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM])

		if payload.get("sub") is None:
			raise credentials_exception

		token_data = User.model_validate({"username": payload.get("sub"), "role": payload.get("role")})

	except JWTError:
		raise credentials_exception

	user = await get_user(username=token_data.username)

	if user is None:
		raise credentials_exception

	return user
