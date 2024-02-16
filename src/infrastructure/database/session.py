from contextvars import ContextVar
from functools import wraps
from typing import Callable, Awaitable, Any

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from infrastructure.config import DatabaseConfig

DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{DatabaseConfig.POSTGRES_USER}'
    f':{DatabaseConfig.POSTGRES_PASSWORD}'
    f'@{DatabaseConfig.POSTGRES_HOST}'
    f':{DatabaseConfig.POSTGRES_PORT}'
    f'/{DatabaseConfig.POSTGRES_DB}'
)

async_engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

ASYNC_CONTEXT_SESSION: ContextVar[AsyncSession] = ContextVar(
    'async_context_session',
)


def in_transaction(func: Callable[[Any], Awaitable[Any]]) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        session: AsyncSession = async_session()
        ASYNC_CONTEXT_SESSION.set(session)

        try:
            result: Any = await func(*args, **kwargs)
            await session.commit()
            return result
        except DatabaseError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except HTTPException as http_exception:
            await session.rollback()
            raise http_exception
        finally:
            await session.close()

    return wrapper
