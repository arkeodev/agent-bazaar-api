from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db.database import async_get_db
from ..core.exceptions.http_exceptions import ForbiddenException, UnauthorizedException
from ..core.logger import logging
from ..core.security import oauth2_scheme, verify_token
from ..crud.crud_users import crud_users

logger = logging.getLogger(__name__)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, Any] | None:
    token_data = await verify_token(token, db)
    if token_data is None:
        raise UnauthorizedException("User not authenticated.")

    if "@" in token_data.username_or_email:
        user: dict | None = await crud_users.get(
            db=db, email=token_data.username_or_email, is_deleted=False
        )
    else:
        user = await crud_users.get(
            db=db, username=token_data.username_or_email, is_deleted=False
        )

    if user:
        return user

    raise UnauthorizedException("User not authenticated.")


async def get_current_superuser(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(async_get_db),
) -> dict:
    token_data = await verify_token(token, db)
    if token_data is None:
        raise HTTPException(status_code=401, detail="User not authenticated.")

    user = await crud_users.get(
        db=db, username=token_data.username_or_email, is_deleted=False
    )
    if user is None or not user.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Not enough privileges.")

    return user
