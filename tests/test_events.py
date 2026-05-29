import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_ingest_event():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/events/", json={
            "event_type": "page_view",
            "user_id": "test_user",
            "page": "/test"
        })
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "queued"
        assert "queue_length" in data

@pytest.mark.asyncio
async def test_ingest_event_minimal():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/events/", json={
            "event_type": "click"
        })
        assert response.status_code == 202

@pytest.mark.asyncio
async def test_ingest_event_missing_type():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/events/", json={
            "user_id": "test_user"
        })
        assert response.status_code == 422