from datetime import datetime
from typing import List, Optional, AsyncGenerator

from sqlalchemy import select, insert, update, Executable
from sqlalchemy.ext.asyncio import AsyncSession

from dto.shift_task import ShiftTaskRequestDTO, ShiftTaskFilterSchema
from infrastructure.database.models import ShiftTask


class ShiftTaskRepository:
    @staticmethod
    def insert_statement(**kwargs) -> Executable:
        """INSERT запрос"""
        return insert(ShiftTask).values(**kwargs).returning(ShiftTask)

    @staticmethod
    def update_statement(*filters, **values_set) -> Executable:
        """Update запрос с фильтрами"""
        return update(ShiftTask).where(*filters).values(**values_set).returning(ShiftTask)

    @staticmethod
    def select_statement(*filters) -> Executable:
        """Простой SELECT запрос с фильтрами"""
        return select(ShiftTask).where(*filters)

    async def create_shift_tasks(
            self,
            session: AsyncSession,
            tasks: List[ShiftTaskRequestDTO]
    ) -> AsyncGenerator[ShiftTask, None]:
        for task in tasks:
            yield await self.create_shift_task(session, task)

    async def create_shift_task(
            self,
            session: AsyncSession,
            task: ShiftTaskRequestDTO
    ) -> ShiftTask:
        """
        Создает новую запись ShiftTask или обновляет существующую,
        если есть запись со значениями batch_number, batch_date переданными в task
        @param session: Асинхронная сессия
        @param task: Pydantic Модель ShiftTask
        @return: ShiftTask
        """
        shift_task: Optional[ShiftTask] = await self.get_shift_task(
            session,
            ShiftTask.batch_date == task.batch_date,
            ShiftTask.batch_number == task.batch_number
        )
        if shift_task:
            return await self.update_shift_task(
                session, shift_task.id,
                **task.model_dump()
            )
        return await session.scalar(self.insert_statement(**task.model_dump()))

    async def get_shift_task(
            self,
            session: AsyncSession,
            *filters
    ) -> Optional[ShiftTask]:
        """
        Возвращает запись ShiftTask или None, если нет записи
        @param session: Асинхронная сессия
        @param filters: Параметры фильтрации
        @return: Optional[ShiftTask]
        """
        return await session.scalar(self.select_statement(*filters))

    async def update_shift_task(
            self,
            session: AsyncSession,
            shift_task_id: int,
            **values_set
    ) -> Optional[ShiftTask]:
        """
        Обновляет запись
        @param session: Асинхронная сессия
        @param shift_task_id: ID Сменного задания
        @param values_set: Новые параметры для установки
        @return: Optional[ShiftTask]
        """
        filters = [ShiftTask.id == shift_task_id]
        if values_set.get('is_closed'):
            closed_at = datetime.utcnow()
            values_set.update({'closed_at': closed_at})
        else:
            values_set.update({'closed_at': None})
        return await session.scalar(self.update_statement(*filters, **values_set))

    async def select_shift_tasks(
            self,
            session: AsyncSession,
            filter_model: ShiftTaskFilterSchema,
            *, limit: int, offset: int
    ) -> AsyncGenerator[ShiftTask, None]:
        """Метод селектит выборку из сменных задач и фильтрует по
        тем фильтрам из ShiftTaskFilterSchema, которые не null"""
        statement: Executable = (
            select(ShiftTask)
            .filter_by(**filter_model.model_dump(exclude_none=True))
            .offset(offset).limit(limit)
        )
        for shift_task in await session.scalars(statement):
            yield shift_task
