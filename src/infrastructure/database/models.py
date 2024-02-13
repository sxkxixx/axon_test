from typing import TypeVar

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

__all__ = [
    'metadata',
    'Base', 'Entity',
]

metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


Entity = TypeVar('Entity', bound=Base)
