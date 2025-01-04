from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from src.common.basedb import DatabasePool
from src.schema.health import GetHealthOut

router = APIRouter()


@router.get("/health", response_model=GetHealthOut)
async def get_health():
	"""
	This endpoint is used to check the health of the service.
	"""
	if DatabasePool.pool.closed:
		return ORJSONResponse(
			status_code=status.HTTP_417_EXPECTATION_FAILED,
			content=GetHealthOut(status="error", message="API is not healthy").model_dump(by_alias=True),
		)

	return GetHealthOut(status="ok", message="API is healthy")
