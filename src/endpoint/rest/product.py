from typing import List, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dto.product import ProductRequestDTO, ProductTableModel, AggregateRequest, UniqueProductID
from infrastructure.database import Product
from infrastructure.database.session import in_transaction, ASYNC_CONTEXT_SESSION
from service.product.service import ProductService
from storage.product.repository import ProductRepository
from storage.shift_task.repository import ShiftTaskRepository

router = APIRouter(prefix='/api/v1', tags=['PRODUCTS'])
product_repository = ProductRepository()
shift_task_repository = ShiftTaskRepository()
product_service = ProductService(shift_task_repository, product_repository)


@router.post('/product')
@in_transaction
async def create_products(
        products: List[ProductRequestDTO]
) -> List[ProductTableModel]:
    session: AsyncSession = ASYNC_CONTEXT_SESSION.get()
    product_response_schemas: List[ProductTableModel] = []
    async for product in product_service.create_products(session, products):
        product_response_schemas.append(
            ProductTableModel.model_validate(product, from_attributes=True)
        )
    return product_response_schemas


@router.patch('/product')
@in_transaction
async def aggregate_product(
        aggregate: AggregateRequest
) -> UniqueProductID:
    session: AsyncSession = ASYNC_CONTEXT_SESSION.get()
    product: Optional[Product] = await product_repository.get_product(
        session,
        Product.product_id == aggregate.product_id
    )
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    if product.shift_task.batch_number != aggregate.batch_number:
        raise HTTPException(status_code=400, detail='Unique code is attached to another batch')
    if product.is_aggregated:
        raise HTTPException(
            status_code=400, detail=f'unique code already used at {product.aggregated_at}')
    await product_repository.aggregate_product(session, product)
    return UniqueProductID(product_id=product.product_id)
