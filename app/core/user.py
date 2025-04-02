from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import logger, MIN_PASSWORD_LENGTH, settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def user_db_in(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


authentication_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_register(
            self, user: User, request: Optional[Request] = None
    ):
        success_message = f'Пользователь {user.email} зарегистрирован.'
        logger.info(success_message)


async def user_manager(user_db=Depends(user_db_in)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    user_manager,
    [authentication_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
