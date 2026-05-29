import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

async def get_token(client: AsyncClient) -> str:
    await client.post("/api/v1/auth/register", json={
        "email": "analytics@example.com",
        "password": "testpass123"
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "analytics@example.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_summary_unauthorized():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/analytics/summary")
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_summary_authorized():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        token = await get_token(client)
        response = await client.get(
            "/api/v1/analytics/summary",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_events" in data
        assert "unique_users" in data
        assert "unique_sessions" in data

@pytest.mark.asyncio
async def test_events_by_type_authorized():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        token = await get_token(client)
        response = await client.get(
            "/api/v1/analytics/events-by-type",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_top_pages_authorized():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        token = await get_token(client)
        response = await client.get(
            "/api/v1/analytics/top-pages",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)