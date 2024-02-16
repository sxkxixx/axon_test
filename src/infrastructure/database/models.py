from datetime import date, datetime
from typing import List

import sqlalchemy
from sqlalchemy import MetaData, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

__all__ = [
    'metadata',
    'Base',
    'ShiftTask',
    'Product'
]

metadata = MetaData()

STR_LENGTH: int = 64


class Base(DeclarativeBase):
    metadata = metadata


class ShiftTask(Base):
    __tablename__ = 'shift_tasks'
    __table_args__ = (
        UniqueConstraint('batch_number', 'batch_date'),
    )

    id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    is_closed: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)
    view_shift_task: Mapped[str] = mapped_column(sqlalchemy.String(length=STR_LENGTH))
    line: Mapped[str] = mapped_column(sqlalchemy.String(length=STR_LENGTH))
    working_shift: Mapped[str] = mapped_column(sqlalchemy.String(length=STR_LENGTH))
    brigade: Mapped[str] = mapped_column(sqlalchemy.String(length=STR_LENGTH))
    batch_number: Mapped[int] = mapped_column(sqlalchemy.Integer)
    batch_date: Mapped[date] = mapped_column(sqlalchemy.Date)
    nomenclature: Mapped[str] = mapped_column(sqlalchemy.String(length=STR_LENGTH))
    csn_code: Mapped[str] = mapped_column(sqlalchemy.String(length=STR_LENGTH))
    distribution_center_id: Mapped[str] = mapped_column(sqlalchemy.String(length=STR_LENGTH))
    shift_start_date: Mapped[datetime] = mapped_column(sqlalchemy.DateTime)
    shift_end_date: Mapped[datetime] = mapped_column(sqlalchemy.DateTime)
    closed_at: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, nullable=True)

    products: Mapped[List['Product']] = relationship('Product', back_populates='shift_task')


class Product(Base):
    __tablename__ = 'products'

    product_id: Mapped[str] = mapped_column(sqlalchemy.String(length=32), primary_key=True)
    shift_task_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey('shift_tasks.id', ondelete='CASCADE')
    )
    is_aggregated: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)
    aggregated_at: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, nullable=True)

    shift_task: Mapped['ShiftTask'] = relationship('ShiftTask', back_populates='products')
