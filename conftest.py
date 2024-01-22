import pytest_asyncio
from async_asgi_testclient import TestClient

from main import app


@pytest_asyncio.fixture(scope='session')
async def client():
    host, port = "127.0.0.1", "8000"
    scope = {"client": (host, port)}

    async with TestClient(
            app, scope=scope
    ) as test_client:
        yield test_client
