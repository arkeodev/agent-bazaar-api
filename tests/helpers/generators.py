import uuid as uuid_pkg

from sqlalchemy.ext.asyncio import AsyncSession

from src.app import models
from src.app.core.security import get_password_hash
from tests.conftest import fake


async def create_user(db: AsyncSession, is_super_user: bool = False) -> models.User:
    """Creates a new user in the database."""
    if not isinstance(db, AsyncSession):
        raise TypeError("db must be an AsyncSession instance")

    _user = models.User(
        name=fake.name(),
        username=fake.user_name(),
        email=fake.email(),
        hashed_password=get_password_hash(fake.password()),
        profile_image_url=fake.image_url(),
        uuid=uuid_pkg.uuid4(),
        is_superuser=is_super_user,
    )

    db.add(_user)
    await db.commit()
    await db.refresh(_user)

    return _user
