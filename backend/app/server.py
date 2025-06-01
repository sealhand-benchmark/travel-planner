from contextlib import asynccontextmanager
from typing import List


from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger
from core.config import env
from api.router import base_router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router=base_router)
    logger.debug("Routers Registered ✔")


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Disposition"],
        ),
        # Middleware(
        #     AuthenticationMiddleware, backend=AuthBackend(), on_error=on_auth_error
        # ),
        # Middleware(SQLAlchemyMiddleware),
        # Middleware(ResponseLogMiddleware),
    ]
    return middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 앱의 start up, shutdown process를 총괄하는 lifespan.
    yield를 기점으로 start up 부분과 shutdown 부분이 나뉨
    """
    logger.info(f'{" App Startup Process ":=^100}')

    # PostgreSQL 연결
    from core.client.postgres import postgres_client

    await postgres_client.init_pool()
    if await postgres_client.is_connected():
        logger.debug(f"[PostreSQL] {env.POSTGRES_DB} Connected ✔")
    else:
        raise ConnectionError(f"[PostreSQL] {env.POSTGRES_DB} connection failed")

    # Redis 연결
    from core.client.redis import redis_client

    if await redis_client.ping():
        logger.debug(f"[Redis] {env.REDIS_HOST} Connected ✔")
    else:
        raise ConnectionError(f"[Redis] {env.REDIS_HOST} connection failed")

    yield

    logger.info(f'{" App Shutdown Process ":=^100}')

    # PostgreSQL 연결 해제
    await postgres_client.close()
    logger.debug(f"[PostgreSQL] {env.POSTGRES_DB} Disconnected ✔")

    # Redis 연결 해제
    try:
        await redis_client.close()
        logger.debug(f"[Redis] {env.REDIS_HOST} Disconnected ✔")
    except Exception as e:
        logger.error(f"[Redis] {env.REDIS_HOST} Disconnection Failed: {e}")

    logger.debug(f'{" App Successfully Shutdown ":=^100}')


def create_app(_lifespan) -> FastAPI:

    logger.info("APP LOADED ENVIRONMENTS: {}".format(env.model_dump()))

    app_ = FastAPI(
        title="Trip Easy Guide",
        description="Trip Easy Guide API",
        version="1.0.0",
        lifespan=_lifespan,
        docks_url=None,
        redoc_url=None,
        # dependencies=[Depends(HTTPLogging)],
        middleware=make_middleware(),
        swagger_ui_parameters={"docExpansion": "none"},
    )

    init_routers(app_)

    return app_


app = create_app(lifespan)
memory_store = {}
