import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app

# Fix event loop for Windows
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c