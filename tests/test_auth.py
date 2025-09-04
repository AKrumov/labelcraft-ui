import pytest
from httpx import AsyncClient
from api.app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/auth/register", json={"email": "a@example.com", "password": "secret"})
        assert resp.status_code == 200
        resp = await ac.post("/api/v1/auth/login", data={"username": "a@example.com", "password": "secret"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token
