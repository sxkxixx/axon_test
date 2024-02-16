from datetime import date
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dto.shift_task import (
    ShiftTaskRequestDTO, ShiftTaskResponseDTO,
    ShiftTaskEditRequestDTO, ShiftTaskFilterSchema
)
from infrastructure.database import ShiftTask
from infrastructure.database.session import in_transaction, ASYNC_CONTEXT_SESSION
from storage.shift_task.repository import ShiftTaskRepository

router = APIRouter(prefix='/api/v1', tags=['SHIFT_TASK'])
shift_task_repository = ShiftTaskRepository()


@router.post('/shift_task')
@in_transaction
async def create_task(
        tasks: List[ShiftTaskRequestDTO],
) -> List[ShiftTaskResponseDTO]:
    session = ASYNC_CONTEXT_SESSION.get()
    created_tasks_list = []
    async for created_task in shift_task_repository.create_shift_tasks(session, tasks):
        created_tasks_list.append(
            ShiftTaskResponseDTO.model_validate(created_task, from_attributes=True)
        )

    return created_tasks_list


@router.get('/shift_task/{_id}')
@in_transaction
async def get_task_by_id(
        _id: int,
) -> Optional[ShiftTaskResponseDTO]:
    session = ASYNC_CONTEXT_SESSION.get()
    shift_task: Optional[ShiftTask] = await shift_task_repository.get_shift_task(
        session, ShiftTask.id == _id)
    if not shift_task:
        return None
    return ShiftTaskResponseDTO.model_validate(shift_task, from_attributes=True)


@router.put('/shift_task/{_id}')
@in_transaction
async def update_shift_task(
        _id: int,
        task: ShiftTaskEditRequestDTO,
) -> ShiftTaskResponseDTO:
    session = ASYNC_CONTEXT_SESSION.get()
    updated_shift_task: Optional[ShiftTask] = await shift_task_repository.update_shift_task(
        session, _id, **task.model_dump(exclude_none=True)
    )
    if not updated_shift_task:
        raise HTTPException(status_code=404, detail="Shift task not found by this id")
    return ShiftTaskResponseDTO.model_validate(updated_shift_task, from_attributes=True)


@router.get('/shift_tasks')
@in_transaction
async def get_filtered_shift_tasks(
        is_closed: Optional[bool] = None,
        batch_number: Optional[int] = None,
        batch_date: Optional[date] = None,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
) -> List[ShiftTaskResponseDTO]:
    session: AsyncSession = ASYNC_CONTEXT_SESSION.get()
    filter_model = ShiftTaskFilterSchema(
        is_closed=is_closed, batch_number=batch_number, batch_date=batch_date
    )
    filtered_shift_tasks: List[ShiftTaskResponseDTO] = []
    async for shift_task in shift_task_repository.select_shift_tasks(
            session, filter_model, limit=limit, offset=offset):
        filtered_shift_tasks.append(
            ShiftTaskResponseDTO.model_validate(shift_task, from_attributes=True))
    return filtered_shift_tasks
