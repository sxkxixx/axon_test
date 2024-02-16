from contextlib import asynccontextmanager

from fastapi import FastAPI

from endpoint.rest import product
from endpoint.rest import shift_task
from infrastructure.database.models import metadata
from infrastructure.database.session import async_engine


@asynccontextmanager
async def database_lifespan(_app: FastAPI):
    async with async_engine.begin() as connect:
        await connect.run_sync(metadata.create_all)
    yield
    async with async_engine.begin() as connect:
        await connect.run_sync(metadata.drop_all)


def _create_app() -> FastAPI:
    _app = FastAPI(lifespan=database_lifespan)
    _app.include_router(shift_task.router)
    _app.include_router(product.router)
    return _app


app = _create_app()
