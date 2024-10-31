import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.crud_agents import crud_agents
from src.app.main import app
from src.app.models.agent import Agent


@pytest.fixture
async def test_agent(db: AsyncSession):
    agent_data = {
        "id": 1,
        "name": "Test Agent",
        "image_path": "/path/to/image.png",
        "description": "A test agent",
        "version": "1.0",
        "creator": "test_creator",
        "port": 8001,
        "status": "stopped",
    }
    agent = await crud_agents.create(db=db, object=agent_data)
    yield agent
    await crud_agents.delete(db=db, id=agent.id)


@pytest.mark.asyncio
async def test_start_agent(test_agent):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/start-agent",
            json={"agent_id": test_agent.id, "docker_image": "test_image"},
        )
        assert response.status_code == 200
        assert "started successfully" in response.json()["message"]


@pytest.mark.asyncio
async def test_stop_agent(test_agent):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/stop-agent", json={"agent_id": test_agent.id}
        )
        assert response.status_code == 200
        assert "stopped successfully" in response.json()["message"]
