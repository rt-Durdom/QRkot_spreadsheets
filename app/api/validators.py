from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import project_crud_chrt
from app.models import CharityProject


async def validate_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    project_id = await project_crud_chrt.get_project_id_by_name(
        name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def validate_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await project_crud_chrt.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!',
        )
    return project


async def validate_invested(
        project_id: int,
        session: AsyncSession
) -> None:
    project = await project_crud_chrt.get(project_id, session)
    if project.invested_amount > 0 or project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def validate_edit(
        full_amount: int,
        project_id: int,
        session: AsyncSession
) -> None:
    project = await project_crud_chrt.get(project_id, session)
    if project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нелья установить значение'
                    ' full_amount меньше уже вложенной суммы.')
        )
