from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router, donation_router, user_router, google_api_router
)

head_router = APIRouter()
head_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['Charity Projects']
)
head_router.include_router(
    donation_router, prefix='/donation', tags=['Donations']
)
head_router.include_router(
    google_api_router, prefix='/google', tags=['Google']
)
head_router.include_router(user_router)
