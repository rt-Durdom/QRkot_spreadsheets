from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.charityproject import project_crud_chrt
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, UserDonationDB
from app.services.services import invest_mode


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Суперюзер может получать список всех пожертвований."""
    all_donations = await donation_crud.multiple(session)
    return all_donations


@router.post(
    '/',
    response_model=UserDonationDB,
    response_model_exclude={'user_id'},
    response_model_exclude_unset=True
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создание нового пожертвования."""
    new_donation = await donation_crud.create(
        donation, session, user, commit=False
    )
    session.add_all(invest_mode(
        new_donation,
        await project_crud_chrt.free_objects(session)
    ))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[UserDonationDB],
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Пользователь может получать список своих пожертвований."""
    all_donations = await donation_crud.get_by_user(user, session)
    return all_donations
