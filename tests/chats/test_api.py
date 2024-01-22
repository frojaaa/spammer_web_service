import pytest
from async_asgi_testclient import TestClient
from fastapi import status
from loguru import logger

from apps.chats.schemas import ChatCreate, Chat


@pytest.mark.asyncio
async def test_get_chats(client: TestClient):
    response = await client.get('/chats')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_read_chat(client: TestClient):
    chat = Chat(id='string', account_id=0)
    response = await client.post('/chats/get_chat', json=chat.model_dump())
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_chats(client: TestClient):
    chat = ChatCreate(id='test', account_id=0)
    response = await client.post("/chats/create", json=[chat.model_dump()])
    assert response.status_code == status.HTTP_201_CREATED and len(response.json()) > 0
    response = await client.post('/chats/get_chat', json=Chat.model_validate(chat.model_dump()).model_dump())
    assert response.status_code == status.HTTP_200_OK
    response = await client.delete(f"/chats/delete", json=chat.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await client.post('/chats/get_chat', json=Chat.model_validate(chat.model_dump()).model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
