import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_portfolio(client, sample_user):
    login_response = await client.post(
        '/auth/login',
        data={'username': sample_user.username, 'password': 'test'},
    )

    assert login_response.status_code == status.HTTP_200_OK

    payload = {
        "portfolio": {"name": "crypto"},
        "coins": [{"coin_id": "ethereum", "amount": 2}],
    }
    resp = await client.post("/portfolio/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    assert "id" in resp.json()
    return resp


@pytest.mark.asyncio
async def test_get_portfolios_list(client, sample_user):
    await test_create_portfolio(client, sample_user)

    resp = await client.get("/portfolio/")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "crypto"
    assert data[0]["coins"][0]["coin_id"] == "ethereum"
    return data[0]['id'], data[0]["coins"][0]['id']


@pytest.mark.asyncio
async def test_get_portfolio_by_id(client, sample_user):
    port_id, _ = await test_get_portfolios_list(client, sample_user)

    resp = await client.get(f"/portfolio/{port_id}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_update_portfolio(client, sample_user):
    port_id, _ = await test_get_portfolios_list(client, sample_user)
    resp = await client.patch(
        f"/portfolio/{port_id}",
        json={
            "update_data": {"name": "updated"},
            "new_coins": [{"coin_id": "cardano", "amount": 10}],
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"] == "Портфель обновлён"


@pytest.mark.asyncio
async def test_delete_portfolio(client, sample_user):
    port_id, _ = await test_get_portfolios_list(client, sample_user)

    resp = await client.delete(f"/portfolio/{port_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"] == "портфель удалён"


@pytest.mark.asyncio
async def test_delete_coin_from_portfolio(client, sample_user):
    port_id, coin_id = await test_get_portfolios_list(client, sample_user)
    
    resp = await client.delete(f"/portfolio/{port_id}/{coin_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"] == "монета удалена из портфеля"


@pytest.mark.asyncio
async def test_get_portfolio_not_found(client, sample_user):
    login_response = await client.post(
        '/auth/login',
        data={'username': sample_user.username, 'password': 'test'},
    )
    assert login_response.status_code == status.HTTP_200_OK

    resp = await client.get("/portfolio/9999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()['detail'] == 'Portfolio not found'
