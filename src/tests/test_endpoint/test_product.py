import httpx
import pytest


@pytest.mark.asyncio
async def test_product_creation(async_client, created_task_id):
    body = [
        {
            'УникальныйКодПродукта': '12gRV60MMsn1',
            'НомерПартии': 22222,
            'ДатаПартии': '2024-01-30',
        },
        {
            "УникальныйКодПродукта": "12gRV60MMsn2",
            "НомерПартии": 33333,
            "ДатаПартии": "2024-01-31"
        }
    ]
    response: httpx.Response = await async_client.post('/api/v1/product', json=body)
    json: list[dict] = response.json()
    product = json[0]
    assert response.status_code == 200
    assert len(json) == 1
    assert product.get('shift_task_id') == created_task_id
    assert product.get('product_id') == '12gRV60MMsn1'


@pytest.mark.asyncio
async def test_product_is_not_aggregated(async_client, created_task_id):
    body = [
        {'УникальныйКодПродукта': '12gRV60MMsn1', 'НомерПартии': 22222, 'ДатаПартии': '2024-01-30'}
    ]
    await async_client.post('/api/v1/product', json=body)
    patch_response: httpx.Response = await async_client.patch('/api/v1/product', json={
        'product_id': '12gRV60MMsn1',
        'batch_number': 22222
    })
    json: dict = patch_response.json()
    assert patch_response.status_code == 200
    assert json.get('product_id') == '12gRV60MMsn1'


@pytest.mark.asyncio
async def test_product_is_aggregated(async_client, created_task_id):
    body = [
        {'УникальныйКодПродукта': '12gRV60MMsn1', 'НомерПартии': 22222, 'ДатаПартии': '2024-01-30'}
    ]
    await async_client.post('/api/v1/product', json=body)
    await async_client.patch(
        '/api/v1/product', json={'product_id': '12gRV60MMsn1', 'batch_number': 22222}
    )
    response: httpx.Response = await async_client.patch(
        '/api/v1/product', json={'product_id': '12gRV60MMsn1', 'batch_number': 22222}
    )
    assert response.status_code == 400, response.content
    json = response.json()
    assert json.get('detail').startswith('unique code already used at')


@pytest.mark.asyncio
async def test_product_with_incorrect_batch_number(async_client, created_task_id):
    body = [
        {'УникальныйКодПродукта': '12gRV60MMsn1', 'НомерПартии': 22222, 'ДатаПартии': '2024-01-30'}
    ]
    await async_client.post('/api/v1/product', json=body)
    response: httpx.Response = await async_client.patch(  # Другой batch_number ⬇
        '/api/v1/product', json={'product_id': '12gRV60MMsn1', 'batch_number': 99999}
    )
    assert response.status_code == 400
    assert response.json().get('detail') == 'Unique code is attached to another batch'


@pytest.mark.asyncio
async def test_product_not_exists(async_client):
    body = [
        {'УникальныйКодПродукта': '12gRV60MMsn1', 'НомерПартии': 22222, 'ДатаПартии': '2024-01-30'}
    ]
    await async_client.post('/api/v1/product', json=body)
    response: httpx.Response = await async_client.patch(
        '/api/v1/product', json={'product_id': '12gRV60MMsn1', 'batch_number': 99999}
        # Другой batch_number
    )
    assert response.status_code == 404
    assert response.json().get('detail') == 'Product not found'
