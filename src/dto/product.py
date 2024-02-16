from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class UniqueProductID(BaseModel):
    product_id: str


class ProductRequestDTO(BaseModel):
    product_id: str = Field(..., validation_alias='УникальныйКодПродукта')
    batch_number: int = Field(..., validation_alias='НомерПартии')
    batch_date: date = Field(..., validation_alias='ДатаПартии')


class ProductTableModel(UniqueProductID):
    shift_task_id: int
    is_aggregated: Optional[bool] = False
    aggregated_at: Optional[datetime] = None


class AggregateRequest(UniqueProductID):
    batch_number: int
