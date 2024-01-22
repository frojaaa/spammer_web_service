import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from apps.proxies.schemas import ProxyCreate
from apps.dependencies import ProxyProtocol


@pytest.mark.asyncio
async def test_get_proxies(client: TestClient):
    response = await client.get('/proxies')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_proxies(client: TestClient):
    proxy = ProxyCreate(protocol=ProxyProtocol.http, host='localhost', username='test', password='test')
    response = await client.post("/proxies/create", json=[proxy.model_dump()])
    assert response.status_code == status.HTTP_201_CREATED and len(response.json()) > 0
    response = await client.get('/proxies')
    assert response.status_code == status.HTTP_200_OK and proxy.model_dump() in response.json()
    response = await client.delete(f"/proxies/delete", json=proxy.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await client.get('/proxies')
    assert response.status_code == status.HTTP_200_OK and proxy.model_dump() not in response.json()
