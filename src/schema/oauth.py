from datetime import datetime

from pydantic import Field

from src.common.basemodel import BaseModel


class PostTokenIn(BaseModel):
	username: str = Field(description="Your username.")
	password: str = Field(description="Your password.")


class PostTokenOut(BaseModel):
	access_token: str = Field(description="The access token, which is used to access the API.")
	token_type: str = Field("bearer", description="The type of the token.")
	expires_in: int = Field(description="The time in seconds until the token expires.")
	expires_at: datetime = Field(description="The time when the token expires.")
