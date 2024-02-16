import httpx
import pytest
import pytest_asyncio

from dto.shift_task import ShiftTaskResponseDTO
from tests.test_endpoint.mocks import MOCK_SHIFT_TASK


@pytest.fixture(scope='function')
async def created_shift_task(async_client) -> ShiftTaskResponseDTO:
    response: httpx.Response = await async_client.post(
        '/api/v1/shift_task', json=[MOCK_SHIFT_TASK]
    )
    return ShiftTaskResponseDTO.model_validate(response.json()[0], from_attributes=True)


@pytest_asyncio.fixture(scope='function')
async def created_task_id(async_client) -> int:
    """
    Создаёт сменную задачу и возвращает её ID
    """
    response: httpx.Response = await async_client.post(
        '/api/v1/shift_task', json=[MOCK_SHIFT_TASK]
    )
    assert response.status_code == 200, response.content
    _id: int = response.json()[0].get('id')
    return _id
