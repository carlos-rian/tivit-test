from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from scalar_fastapi import get_scalar_api_reference

from src.common.basedb import DatabasePool, Settings
from src.common.helper import initialize_users
from src.resource import health, oauth, user


@asynccontextmanager
async def lifecycle(app: FastAPI):
	await DatabasePool.start()
	await initialize_users(pool=DatabasePool)
	yield
	await DatabasePool.stop()


def create_app():
	app = FastAPI(
		default_response_class=ORJSONResponse,
		lifespan=lifecycle,
		title=Settings.API_TITLE,
		version=Settings.API_VERSION,
	)

	app.add_middleware(middleware_class=GZipMiddleware)
	app.add_middleware(
		middleware_class=CORSMiddleware,
		allow_origins=Settings.API_CORS_ORIGINS,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
	# Include routers, which are the endpoints of the API.
	app.include_router(health.router, prefix=Settings.API_PREFIX)
	app.include_router(oauth.router, prefix=Settings.API_PREFIX)
	app.include_router(user.router, prefix=Settings.API_PREFIX)

	# Include the Scalar API reference.
	@app.get("/scalar", include_in_schema=False)
	def get_scalar():
		return get_scalar_api_reference(
			openapi_url=app.openapi_url,
			title=app.title,
		)

	return app
