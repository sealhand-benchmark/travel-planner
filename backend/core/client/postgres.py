from typing import AsyncGenerator
from psycopg_pool import AsyncConnectionPool
from psycopg.connection_async import AsyncConnection
from core.config import env
from loguru import logger


class PostgresClient:
    _instance = None
    _pool: AsyncConnectionPool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresClient, cls).__new__(cls)
        return cls._instance

    async def init_pool(self):
        if self._pool is None:
            conninfo = f"host={env.POSTGRES_HOST} port={env.POSTGRES_PORT} user={env.POSTGRES_USER} password={env.POSTGRES_PASSWORD} dbname={env.POSTGRES_DB}"
            self._pool = AsyncConnectionPool(
                conninfo, min_size=5, max_size=20, kwargs={"autocommit": True}
            )
            logger.info("PostgreSQL connection pool initialized")

    async def close(self):
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("PostgreSQL connection pool closed")

    async def get_connection(self) -> AsyncConnectionPool:
        if not self._pool:
            await self.init_pool()
        return self._pool

    async def is_connected(self) -> bool:
        try:
            async with self._pool as pool:
                async with pool.connection() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"PostgreSQL connection check failed: {e}")
            return False


# 싱글톤 인스턴스 생성
postgres_client = PostgresClient()


# FastAPI 의존성
async def get_db() -> AsyncGenerator[AsyncConnection, None]:
    """
    FastAPI 의존성으로 사용할 데이터베이스 연결을 제공합니다.
    """
    pool = await postgres_client.get_connection()
    async with pool.connection() as connection:
        try:
            yield connection
        finally:
            # connection은 pool.connection()의 컨텍스트 매니저에 의해 자동으로 반환됩니다
            pass
