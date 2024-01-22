import pytest
from async_asgi_testclient import TestClient
from fastapi import status
from loguru import logger

from apps.subscriptions.schemas import SubscriptionCreate


@pytest.mark.asyncio
async def test_get_subscriptions(client: TestClient):
    response = await client.get('/subscriptions')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_subscriptions(client: TestClient):
    subscription = SubscriptionCreate(chat_id='test', account_id=0)
    response = await client.post("/subscriptions/create", json=[subscription.model_dump()])
    assert response.status_code == status.HTTP_201_CREATED and len(response.json()) > 0
    response = await client.get('/subscriptions')
    assert response.status_code == status.HTTP_200_OK and subscription.model_dump() in response.json()
    response = await client.delete(f"/subscriptions/delete", json=subscription.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await client.get('/subscriptions')
    assert response.status_code == status.HTTP_200_OK and subscription.model_dump() not in response.json()
