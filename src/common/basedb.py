from pysqlx_engine import PySQLXEnginePool

from src.config.settings import Settings


class DatabasePool:
	"""
	BaseDB class for handling database operations.

	This class provides a connection to a database using the PySQLXEngine and includes methods for connecting to the database.
	"""

	pool = PySQLXEnginePool(
		uri=Settings.DATABASE_URI,
		min_size=Settings.DATABASE_POOL_MIN_SIZE,
		max_size=Settings.DATABASE_POOL_MAX_SIZE,
	)

	@classmethod
	async def start(cls):
		await cls.pool.start()

	@classmethod
	async def stop(cls):
		await cls.pool.stop()
