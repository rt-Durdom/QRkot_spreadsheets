from fastapi import APIRouter

from app.core.user import authentication_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(authentication_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    r for r in users_router.routes if r.name != 'users:delete_user'
]
router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)
