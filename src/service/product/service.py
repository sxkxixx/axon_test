from typing import List, Optional, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from dto.product import ProductRequestDTO, ProductTableModel
from infrastructure.database import ShiftTask, Product
from storage.product.repository import ProductRepository
from storage.shift_task.repository import ShiftTaskRepository


class ProductService:
    def __init__(
            self,
            shift_task_repository: ShiftTaskRepository,
            product_repository: ProductRepository,
    ):
        """
        :param shift_task_repository: Репозиторий для ShiftTask
        :param product_repository: Репозиторий для Product
        """
        self.shift_task_repository = shift_task_repository
        self.product_repository = product_repository

    async def create_products(
            self,
            session: AsyncSession,
            products: List[ProductRequestDTO]
    ) -> AsyncGenerator[Product, None]:
        """
        Генератор для создания списка продукции.
        Если продукция не была создана (метод create_product вернул None), то
        генератор не возвращает значение
        """
        for product in products:
            product = await self.create_product(session, product)
            if product:
                yield product

    async def create_product(
            self,
            session: AsyncSession,
            product: ProductRequestDTO
    ) -> Optional[Product]:
        """
        Создаёт продукцию и возвращает запись,
        возвращает None если нет записи ShiftTask с указанными batch_date и batch_number
        """
        shift_task: Optional[ShiftTask] = await self.shift_task_repository.get_shift_task(
            session,
            ShiftTask.batch_date == product.batch_date,
            ShiftTask.batch_number == product.batch_number)
        if not shift_task:
            return None
        schema = ProductTableModel(
            product_id=product.product_id,
            shift_task_id=shift_task.id
        )
        return await self.product_repository.create_product(session, schema)
