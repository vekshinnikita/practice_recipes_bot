from sqlalchemy import select
from app.models.recipe import Admin, Ingredient, Tag
from app.models.base import async_session


class AdminRepo:

    @classmethod
    async def is_admin(cls, tg_id: int):
        async with async_session() as session:
            query = (
                select(Admin)
                    .filter(Admin.tg_id == tg_id)
            )

            return (await session.execute(query)).first() is not None
    
    @classmethod
    async def set_admin(cls, tg_id: int):
        async with async_session() as session:
            new_admin = Admin(tg_id=tg_id)
            session.add(new_admin)
            await session.commit()

    
