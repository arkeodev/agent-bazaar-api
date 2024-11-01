from collections.abc import Callable
from typing import Any

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.config import settings
from src.app.main import app

DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_ASYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

# Create an asynchronous engine
async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Configure the session maker to use AsyncSession
async_session_maker = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)

fake = Faker()


@pytest.fixture(scope="function")
async def db() -> AsyncSession:
    """Fixture that provides a scoped session per test function."""
    async with async_session_maker() as session:
        yield session  # Ensures an actual AsyncSession is yielded
        await session.rollback()  # Clean up any changes after each test


@pytest.fixture(scope="session", autouse=True)
async def dispose_engine():
    yield
    await async_engine.dispose()


def override_dependency(dependency: Callable[..., Any], mocked_response: Any) -> None:
    app.dependency_overrides[dependency] = lambda: mocked_response
