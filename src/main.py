from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from guvicorn_logger import Logger as _Logger
from scalar_fastapi import get_scalar_api_reference

from src.common.basedb import DatabasePool, Settings
from src.common.helper import initialize_users
from src.resource import health, oauth, user


def setup_logger():
	format = "[%(correlation_id)s] [%(pid)s] [%(filename)s:%(lineno)s] | %(levelprefix)s %(message)s"
	_Logger(fmt=format, correlation_id=True, use_colors=Settings.is_dev).configure()

	if Settings.is_dev:
		import logging

		from pysqlx_engine import LOG_CONFIG

		from src.common.logger import Logger

		LOG_CONFIG.PYSQLX_SQL_LOG = True
		LOG_CONFIG.PYSQLX_USE_COLOR = True
		LOG_CONFIG.PYSQLX_ERROR_JSON_FMT = True

		Logger.setLevel(logging.DEBUG)

		Logger.debug("Logger is set up in development mode.")


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
	setup_logger()

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
