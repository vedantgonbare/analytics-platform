import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        assert response.status_code in [201, 400]  # 400 if already exists

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Register first
        await client.post("/api/v1/auth/register", json={
            "email": "logintest@example.com",
            "password": "testpass123"
        })
        # Then login
        response = await client.post("/api/v1/auth/login", json={
            "email": "logintest@example.com",
            "password": "testpass123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_wrong_password():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/api/v1/auth/login", json={
            "email": "logintest@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_me_without_token():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 403