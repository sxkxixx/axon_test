import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from infrastructure.database.models import metadata
from infrastructure.database.session import async_engine
from main import app


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://testserver') as ac:
        yield ac


@pytest_asyncio.fixture(scope='function', autouse=True)
async def init_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
