import pytest
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.dependencies import get_current_superuser
from src.app.crud.crud_agents import crud_agents
from src.app.main import app
from src.app.models.agent import Agent, AgentStatus


@pytest.fixture
async def test_agent(db: AsyncSession):
    agent_data = {
        "name": "Test Agent",
        "image_path": "/path/to/image.png",
        "description": "A test agent",
        "version": "1.0",
        "creator": "test_creator",
        "port": 8001,
        "status": AgentStatus.STOPPED,
    }
    agent = await crud_agents.create(db=db, object=agent_data)
    yield agent
    await crud_agents.delete(db=db, id=agent.id)


@pytest.fixture
def override_get_current_superuser():
    def mock_get_current_superuser():
        return {"username": "test_superuser", "is_superuser": True}

    app.dependency_overrides[get_current_superuser] = mock_get_current_superuser
    yield
    app.dependency_overrides.pop(get_current_superuser, None)


@pytest.mark.asyncio
async def test_start_agent(test_agent, override_get_current_superuser):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/start-agent",
            params={"agent_id": "1", "docker_image": "test_image"},
        )
        print(response.json())
        assert response.status_code == 200
        assert "started successfully" in response.json()["message"]


@pytest.mark.asyncio
async def test_stop_agent(test_agent, override_get_current_superuser):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/stop-agent", params={"agent_id": "1"})
        assert response.status_code == 200
        assert "stopped successfully" in response.json()["message"]
