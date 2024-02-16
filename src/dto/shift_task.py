from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ShiftTaskRequestDTO(BaseModel):
    """Статус закрытия"""
    is_closed: bool = Field(..., validation_alias='СтатусЗакрытия')

    """Представление Задания На Смену"""
    view_shift_task: str = Field(..., validation_alias='ПредставлениеЗаданияНаСмену')

    """Линия / Рабочий Центр"""
    line: str = Field(..., validation_alias='Линия')

    """Смена"""
    working_shift: str = Field(..., validation_alias='Смена')

    """Бригада"""
    brigade: str = Field(..., validation_alias='Бригада')

    """Номер партии"""
    batch_number: int = Field(..., validation_alias='НомерПартии')

    """Дата партии"""
    batch_date: date = Field(..., validation_alias='ДатаПартии')

    """Номеклатура"""
    nomenclature: str = Field(..., validation_alias='Номенклатура')

    """КОД ЕКН"""
    csn_code: str = Field(..., validation_alias='КодЕКН')

    """Идентификатор РЦ"""
    distribution_center_id: str = Field(..., validation_alias='ИдентификаторРЦ')

    """Дата и время начала смены"""
    shift_start_date: datetime = Field(..., validation_alias='ДатаВремяНачалаСмены')

    """Дата и время окончания смены"""
    shift_end_date: datetime = Field(..., validation_alias='ДатаВремяОкончанияСмены')


class ShiftTaskFilterSchema(BaseModel):
    is_closed: Optional[bool] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None


class ShiftTaskEditRequestDTO(ShiftTaskFilterSchema):
    view_shift_task: Optional[str] = None
    line: Optional[str] = None
    working_shift: Optional[str] = None
    brigade: Optional[str] = None
    nomenclature: Optional[str] = None
    csn_code: Optional[str] = None
    distribution_center_id: Optional[str] = None
    shift_start_date: Optional[datetime] = None
    shift_end_date: Optional[datetime] = None


class ShiftTaskResponseDTO(BaseModel):
    id: int
    is_closed: bool
    view_shift_task: str
    line: str
    working_shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    csn_code: str
    distribution_center_id: str
    shift_start_date: datetime
    shift_end_date: datetime
    closed_at: Optional[datetime] = None
