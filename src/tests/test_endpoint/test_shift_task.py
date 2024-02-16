from datetime import datetime

import httpx
import pytest

from .mocks import UPDATED_MOCK_TASK


@pytest.mark.asyncio
async def test_shift_task_merge_created(async_client, created_task_id):
    """
    Проверяет что создание сменной задачи с НЕуникальными batch_number и batch_date
    перезапишет существующую запись в БД
    """
    await async_client.post(
        '/api/v1/shift_task',
        json=[dict(
            СтатусЗакрытия=False, ПредставлениеЗаданияНаСмену='Задание на смену 34324234',
            Линия='Т3', Смена='2', Бригада='Бригада №4',
            # Номер партии и дата партии равны тем же полям в MOCK_SHIFT_TASK
            НомерПартии='22222', ДатаПартии='2024-01-30',
            Номенклатура='Какая то номенклатура', КодЕКН='456678', ИдентификаторРЦ='B',
            ДатаВремяНачалаСмены='2024-01-30T20:00:00',
            ДатаВремяОкончанияСмены='2024-01-31T08:00:00',
        )]
    )
    # GET-запрос на ту запись, которая была создана первой
    json_response = (await async_client.get(f'/api/v1/shift_task/{created_task_id}')).json()
    assert json_response.get('view_shift_task') == 'Задание на смену 34324234'
    assert json_response.get('distribution_center_id') == 'B'
    assert json_response.get('batch_number') == 22222
    assert json_response.get('batch_date') == '2024-01-30'


@pytest.mark.asyncio
async def test_shift_task_creating(async_client, created_task_id):
    """Тестирует, что все переданные данные будут созданы"""
    get_response: httpx.Response = await async_client.get(f'/api/v1/shift_task/{created_task_id}')
    assert get_response.status_code == 200
    get_response_json = get_response.json()
    assert get_response_json.get('id') == created_task_id
    assert get_response_json.get('nomenclature') == 'Какая то номенклатура'


@pytest.mark.asyncio
async def test_shift_task_updating(created_task_id, async_client):
    """
    Проверяет что сменная задача будет обновлена
    """
    # Запрос на обновление
    await async_client.put(
        f'/api/v1/shift_task/{created_task_id}',
        json=UPDATED_MOCK_TASK
    )
    # GET-запрос
    response: httpx.Response = await async_client.get(f'/api/v1/shift_task/{created_task_id}')
    json_response: dict = response.json()
    # Поле осталось без изменений
    assert not json_response.get('is_closed')
    # closed_at остался None
    assert json_response.get('closed_at') is None
    # Проверка нескольких полей на изменение
    assert json_response.get('line') == 'Т5'
    assert json_response.get('nomenclature') == 'Изменённая номеклатура'


@pytest.mark.asyncio
async def test_shift_task_get_closed_at(created_task_id, async_client):
    """
    Проверяет что при обновлении поля is_closed на True
    у сменной задачи появляется поле closed_at
    """
    await async_client.put(
        f'/api/v1/shift_task/{created_task_id}', json={'is_closed': True}
    )
    response = await async_client.get(f'/api/v1/shift_task/{created_task_id}')
    json_response: dict = response.json()
    assert json_response.get('is_closed')
    today = datetime.utcnow().timestamp()
    updated_closed_at = datetime.fromisoformat(json_response.get('closed_at')).timestamp()
    assert abs(today - updated_closed_at) < 20, abs(today - updated_closed_at)


@pytest.mark.asyncio
async def test_shift_task_closed_at_none(created_task_id, async_client):
    """
    Проверяет что при смене поля is_closed со значения True на значение False
    у меня сменной задачи поле closed_at будет равно None (null)
    """
    is_closed_true_response: dict = (await async_client.put(
        f'/api/v1/shift_task/{created_task_id}', json={'is_closed': True}
    )).json()
    assert is_closed_true_response.get('is_closed') and is_closed_true_response.get('closed_at')

    is_closed_false_response: dict = (
        await async_client.put(
            f'/api/v1/shift_task/{created_task_id}', json={'is_closed': False}
        )).json()

    assert not (
            is_closed_false_response.get('is_closed')
            and is_closed_false_response.get('closed_at')
    )
