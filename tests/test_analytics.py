import pytest
from unittest.mock import AsyncMock, MagicMock, patch

def make_mock_db(summary=None, list_result=None):
    mock_result = MagicMock()
    if summary:
        mock_result.one.return_value = summary
    if list_result is not None:
        mock_result.__iter__ = MagicMock(return_value=iter(list_result))
    mock_db = AsyncMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    return mock_db

async def test_summary_unauthorized(client):
    response = await client.get("/api/v1/analytics/summary")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_events_endpoint_exists(client):
    with patch("app.services.event_service.redis_client") as mock_redis:
        mock_redis.lpush = AsyncMock(return_value=1)
        response = await client.post("/api/v1/events/", json={
            "event_type": "test_event"
        })
    assert response.status_code == 202

@pytest.mark.asyncio
async def test_analytics_requires_auth(client):
    endpoints = [
        "/api/v1/analytics/summary",
        "/api/v1/analytics/events-by-type",
        "/api/v1/analytics/events-over-time",
        "/api/v1/analytics/top-pages",
    ]
    for endpoint in endpoints:
        response = await client.get(endpoint)
        assert response.status_code != 200, f"{endpoint} should require auth"