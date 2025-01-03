from fastapi import APIRouter

from src.common.basedb import DatabasePool
from src.schema.health import GetHealthOut

router = APIRouter()


@router.get("/health", response_model=GetHealthOut)
async def get_health():
	"""
	This endpoint is used to check the health of the service.
	"""
	if DatabasePool.pool.closed:
		return GetHealthOut(status="error", message="API is not healthy")

	return GetHealthOut(status="ok", message="API is healthy")
