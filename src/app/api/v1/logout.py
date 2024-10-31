import docker
from fastapi import APIRouter, Depends, HTTPException, Response
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import UnauthorizedException
from ...core.security import blacklist_token, oauth2_scheme

router = APIRouter(tags=["login"])

client = docker.from_env()


@router.post("/logout", status_code=201)
async def logout(
    response: Response,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(async_get_db),
) -> dict[str, str]:
    try:
        await blacklist_token(token=access_token, db=db)
        response.delete_cookie(key="refresh_token")

        return {"message": "Logged out successfully"}

    except JWTError:
        raise UnauthorizedException("Invalid token.")


@router.post("/exit-agentic-app")
async def exit_agentic_app(
    agent_id: str, current_user: dict = Depends(get_current_superuser)
):
    try:
        # Logic to stop the agentic app container
        container = client.containers.get(agent_id)
        container.stop()
        return {"message": f"Agentic app {agent_id} stopped successfully"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Agentic app not found")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
