from os import getenv
from uuid import uuid4


def get_cors_origins() -> list[str]:
	origins = getenv("API_CORS_ORIGINS", "").split(",")
	origins = [origin.strip() for origin in origins if origin.strip()]
	return origins or ["http://localhost", "http://localhost:3000", "http://localhost:8000"]


class Settings:
	DATABASE_URI: str = getenv("DATABASE_URI")
	DATABASE_POOL_MIN_SIZE: int = int(getenv("DATABASE_POOL_MIN_SIZE", 2))
	DATABASE_POOL_MAX_SIZE: int = int(getenv("DATABASE_POOL_MAX_SIZE", 10))

	JWT_SECRET_KEY: str | None = getenv("JWT_SECRET_KEY", uuid4().hex)
	JWT_ALGORITHM: str = "HS256"
	JWT_EXPIRE_MINUTES: int = 30

	API_PREFIX: str = "/fake"
	API_TITLE: str = "TIVIT API"
	API_VERSION: str = "0.1.0"
	API_DESCRIPTION: str = "API for TIVIT Recruitment Process"
	API_CORS_ORIGINS: list[str] = get_cors_origins()
