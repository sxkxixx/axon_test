from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dto.product import ProductTableModel
from infrastructure.database import Product


class ProductRepository:
    async def create_product(self, session: AsyncSession, product: ProductTableModel) -> Product:
        """Метод создаёт Product и возвращает запись"""
        statement = (
            insert(Product).values(**product.model_dump()).returning(Product)
        )
        return await session.scalar(statement)

    async def get_product(self, session: AsyncSession, *filters) -> Optional[Product]:
        """Метод возвращает Product и отношением shift_task (ShiftTask) или None, если нет записи
        с указанными значениями из *filters
        """
        statement = (
            select(Product).where(*filters).options(selectinload(Product.shift_task))
        )
        return await session.scalar(statement)

    async def aggregate_product(self, session: AsyncSession, product: Product) -> None:
        """
        Агрегирует запись product:
        Устанавливает is_aggregated на значение True, aggregated_at на текущее время
        """
        product.is_aggregated = True
        product.aggregated_at = datetime.utcnow()
        session.add(product)
