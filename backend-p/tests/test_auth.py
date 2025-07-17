import pytest
from fastapi import status

user_data = {
    'username': 'test',
    'email': 'testuser@nofoobar.com',
    'password': 'testing',
}


@pytest.mark.asyncio
async def test_user_registration(client):
    response = await client.post('/auth/register', json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.cookies
    assert 'access_token' in response.json()

    return response


@pytest.mark.asyncio
async def test_user_login(client):
    response = await test_user_registration(client)

    assert 'access_token' in response.cookies
    login_response = await client.post(
        '/auth/login',
        data={'username': user_data['username'], 'password': user_data['password']},
    )

    assert login_response.status_code == status.HTTP_200_OK
    assert 'access_token' in login_response.json()
    assert 'access_token' in login_response.cookies
    return login_response


@pytest.mark.asyncio
async def test_get_me(client):
    response = await test_user_login(client)

    assert 'access_token' in response.cookies
    response = await client.get('/user/me')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['username'] == 'test'
    assert 'password' not in data


@pytest.mark.asyncio
async def test_refresh(client):
    response = await test_user_login(client)

    assert 'access_token' in response.cookies

    client.cookies.delete('access_token')
    assert 'access_token' not in client.cookies
    response_refresh = await client.post('/auth/refresh')
    assert 'access_token' in response_refresh.cookies


@pytest.mark.asyncio
async def test_logout(client):
    response = await test_user_login(client)

    assert 'access_token' in response.cookies

    response_refresh = await client.post('/auth/logout')
    assert 'access_token' not in response_refresh.cookies
    assert 'refresh_token' not in response_refresh.cookies
