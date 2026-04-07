from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.test import test_router
from core.logger import LOGGING_CONFIG, logger
from core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    yield


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов приложения."""
    app.include_router(test_router, prefix="/api/v1/test", tags=["test"])


def create_app() -> FastAPI:
    """Фабрика для создания приложения."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    setup_routes(app)
    return app


def start_server() -> None:
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        # log_config=LOGGING_CONFIG,
        log_level=settings.LOG_LEVEL.lower(),
        reload=True, # settings.APP_RELOAD,
    )


app = create_app()


if __name__ == "__main__":
    logger.info("Starting server...")
    start_server()
