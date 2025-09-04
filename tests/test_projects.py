import pytest
from httpx import AsyncClient
from api.app.main import app


@pytest.mark.asyncio
async def test_create_and_list_projects():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # register and login
        await ac.post("/api/v1/auth/register", json={"email": "p@example.com", "password": "secret"})
        resp = await ac.post(
            "/api/v1/auth/login",
            data={"username": "p@example.com", "password": "secret"},
        )
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # create project
        resp = await ac.post("/api/v1/projects", json={"name": "proj1"}, headers=headers)
        assert resp.status_code == 200

        # list projects
        resp = await ac.get("/api/v1/projects", headers=headers)
        assert any(p["name"] == "proj1" for p in resp.json())
