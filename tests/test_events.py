import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_ingest_event(client):
    with patch("app.services.event_service.redis_client") as mock_redis:
        mock_redis.lpush = AsyncMock(return_value=1)
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
async def test_ingest_event_minimal(client):
    with patch("app.services.event_service.redis_client") as mock_redis:
        mock_redis.lpush = AsyncMock(return_value=1)
        response = await client.post("/api/v1/events/", json={
            "event_type": "click"
        })
    assert response.status_code == 202

@pytest.mark.asyncio
async def test_ingest_event_missing_type(client):
    response = await client.post("/api/v1/events/", json={
        "user_id": "test_user"
    })
    assert response.status_code == 422