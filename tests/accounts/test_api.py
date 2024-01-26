import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from apps.accounts.schemas import AccountCreate


@pytest.mark.asyncio
async def test_get_accounts(client: TestClient):
    response = await client.get('/accounts')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_read_account(client: TestClient):
    response = await client.get('/accounts/0')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_accounts(client: TestClient):
    account = AccountCreate(id=12345678, api_hash='test', name='test', project_id=0)
    response = await client.post("/accounts/create", json=[account.model_dump()])
    assert response.status_code == status.HTTP_201_CREATED and len(response.json()) > 0
    response = await client.get(f"/accounts/{account.id}")
    assert response.status_code == status.HTTP_200_OK
    response = await client.delete(f"/accounts/{account.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await client.get(f"/accounts/{account.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
