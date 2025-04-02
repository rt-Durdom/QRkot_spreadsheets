from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import project_crud_chrt
from app.crud.donation import donation_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.services import invest_mode
from app.api.validators import (validate_duplicate,
                                validate_project_exists,
                                validate_invested,
                                validate_edit)
from app.core.user import current_superuser


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    projects = await project_crud_chrt.multiple(session)
    return projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Суперюзер может удалять любой проект."""
    project = await validate_project_exists(project_id, session)
    await validate_invested(project_id, session)
    deleted_project = await project_crud_chrt.remove(project, session)
    return deleted_project


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Суперюзер может создавать любой проект."""
    await validate_duplicate(project.name, session)
    new_project = await project_crud_chrt.create(
        project, session, commit=False
    )

    session.add_all(invest_mode(
        new_project,
        await donation_crud.free_objects(session)
    ))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Суперюзер может редактировать любой проект."""
    project = await validate_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await validate_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await validate_edit(
            obj_in.full_amount, project_id, session
        )
    up_project = await project_crud_chrt.update(
        project, obj_in, session
    )
    await session.commit()
    await session.refresh(up_project)
    return up_project
