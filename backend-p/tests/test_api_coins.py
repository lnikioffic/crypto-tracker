import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_coins_list(client):
    response = await client.get('/coins/')

    assert response.status_code == status.HTTP_200_OK
    assert 100 == len(response.json())


@pytest.mark.asyncio
async def test_get_coins_list_name(client):
    response = await client.get('/coins/names')
    assert response.status_code == status.HTTP_200_OK
    assert 0 < len(response.json())


@pytest.mark.parametrize(
    'coin_id,expected_status',
    [
        ('bitcoin', status.HTTP_200_OK),
        ('ethereum', status.HTTP_200_OK),
        ('bitcoin,ethereum', status.HTTP_422_UNPROCESSABLE_ENTITY),
        ('unknowncoin', status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_get_coin(client, coin_id, expected_status):
    response = await client.get(f'/coins/{coin_id}')

    assert response.status_code == expected_status
    data = response.json()
    if expected_status == status.HTTP_200_OK:
        assert data['id'] == coin_id
