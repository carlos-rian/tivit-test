from fastapi import APIRouter, Query

from src.schema.oauth import PostTokenIn, PostTokenOut
from src.service.oauth import OAuthService

router = APIRouter()


@router.post("/token", response_model=PostTokenOut)
async def post_token(
	username: str = Query(
		min_length=4,
		max_length=256,
		description="Your username must be at least 4 characters long and at most 256 characters long.",
	),
	password: str = Query(
		min_length=8,
		max_length=256,
		description="Your password must be at least 8 characters long and at most 256 characters long.",
	),
):
	"""
	This endpoint is used to get an access token.

	You must provide a username and password to get an access token.

	The username and password are provided as query parameters.

	**username**: Your username (min length: 4, max length: 256).

	**password**: Your password (min length: 8, max length: 256).
	"""

	return await OAuthService.post_token(PostTokenIn(username=username, password=password))
