from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def free_objects(
            self,
            session: AsyncSession,
    ):
        result = await session.execute(
            select(self.model).filter(self.model.fully_invested.is_(False))
        )
        return result.scalars().all()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        return (await session.execute(select(self.model).where(
                self.model.id == obj_id))).scalars().first()

    async def multiple(
            self,
            session: AsyncSession
    ):
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
        self,
        object_in,
        session: AsyncSession,
        user: Optional[User] = None,
        commit: bool = True
    ):
        object_data = object_in.dict()
        if user is not None:
            object_data['user_id'] = user.id
        db_object = self.model(**object_data)
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object

    async def update(
            self,
            db_object,
            object_in,
            session: AsyncSession,
            commit: bool = True
    ):
        obj_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        return (await session.execute(select(self.model)
                .where(attr == attr_value))).scalars().first()
