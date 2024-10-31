import asyncio

import pytest
from fastapi import status
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_current_user
from src.app.api.v1.users import oauth2_scheme
from src.app.main import app
from tests.conftest import fake, override_dependency

from .helpers import generators, mocks


@pytest.mark.asyncio
async def test_post_user(client: AsyncClient) -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/user",
            json={
                "name": fake.name(),
                "username": fake.user_name(),
                "email": fake.email(),
                "password": fake.password(),
            },
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_user(db: Session, client: AsyncClient) -> None:
    user = generators.create_user(db)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/api/v1/user/{user.username}")
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data["id"] == user.id
        assert response_data["username"] == user.username


@pytest.mark.asyncio
async def test_get_multiple_users(db: Session, client: AsyncClient) -> None:
    for _ in range(5):
        generators.create_user(db)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/users")
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()["data"]
        assert len(response_data) >= 5


@pytest.mark.asyncio(scope="session")
async def test_update_user(db: Session, client: AsyncClient) -> None:
    user = generators.create_user(db)
    new_name = fake.name()

    override_dependency(get_current_user, mocks.get_current_user(user))

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch(
            f"/api/v1/user/{user.username}", json={"name": new_name}
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_user(
    db: Session, client: AsyncClient, mocker: MockerFixture
) -> None:
    user = generators.create_user(db)

    override_dependency(get_current_user, mocks.get_current_user(user))
    override_dependency(oauth2_scheme, mocks.oauth2_scheme())

    mocker.patch(
        "src.app.core.security.jwt.decode",
        return_value={"sub": user.username, "exp": 9999999999},
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/api/v1/user/{user.username}")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_db_user(
    db: Session, mocker: MockerFixture, client: AsyncClient
) -> None:
    user = generators.create_user(db)
    super_user = generators.create_user(db, is_super_user=True)

    override_dependency(get_current_user, mocks.get_current_user(super_user))
    override_dependency(oauth2_scheme, mocks.oauth2_scheme())

    mocker.patch(
        "src.app.core.security.jwt.decode",
        return_value={"sub": super_user.username, "exp": 9999999999},
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/api/v1/db_user/{user.username}")
        assert response.status_code == status.HTTP_200_OK
