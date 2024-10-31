import docker
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.port_manager import PortManager

router = APIRouter()

client = docker.from_env()
port_manager = PortManager()


@router.post("/start-agent")
async def start_agent(
    agent_id: str,
    docker_image: str,
    current_user: dict = Depends(get_current_superuser),
):
    try:
        # Pull the image if not already available
        client.images.pull(docker_image)

        # Get an available port
        port = port_manager.get_available_port()

        # Start the container
        container = client.containers.run(
            docker_image, detach=True, ports={"80/tcp": port}, name=f"agent_{agent_id}"
        )

        return {
            "message": f"Agentic app {agent_id} started successfully on port {port}"
        }

    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/stop-agent")
async def stop_agent(
    agent_id: str, current_user: dict = Depends(get_current_superuser)
):
    try:
        # Get the container by name
        container = client.containers.get(f"agent_{agent_id}")
        container.stop()
        container.remove()

        # Release the port
        port_manager.release_port(
            container.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
        )

        return {"message": f"Agentic app {agent_id} stopped successfully"}

    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Agentic app not found")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
