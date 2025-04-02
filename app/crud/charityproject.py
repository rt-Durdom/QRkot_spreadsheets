from typing import Optional

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        return (await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )).scalars().first()

    async def get_projects_by_completion_rate(
        session: AsyncSession
    ) -> list[CharityProject]:

        result = extract(
            'epoch', CharityProject.close_date
        ) - extract('epoch', CharityProject.create_date)

        return (
            await session.execute(
                select(CharityProject).where(CharityProject.fully_invested)
            ).order_by(result)
        ).scalars().all()


project_crud_chrt = CRUDCharityProject(CharityProject)
