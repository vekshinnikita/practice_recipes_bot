from typing import List
from sqlalchemy import func, select
from app.models.recipe import Recipe, Tag
from app.models.base import async_session
from app.types.pagination import PaginatedResult

class TagRepo:

    @classmethod
    async def add_tag(cls, name: str):
        async with async_session() as session:
            tag = Tag(name=name)
            session.add(tag)
            await session.commit()
    
    @classmethod
    async def get_tags_by_ids(cls, ids: List[int]) -> List[Tag]:
        if not ids:
            return []
        
        async with async_session() as session:
            query = (
                select(Tag)
                .filter(
                    Tag.id.in_(ids)
                )
            )

            return list(await session.scalars(query))

    @classmethod
    async def get_tag_by_name(cls, name: str):
        async with async_session() as session:
            query = (
                select(Tag)
                .filter(
                    Tag.name == name
                )
            )

            return await session.scalar(query)
    
    @classmethod
    async def get_tags(cls, offset: int, limit:int):
        async with async_session() as session:
            query = (
                select(Tag)
                .order_by(Tag.name)
                .offset(offset)
                .limit(limit)
            )
            query_count = select(func.count(Tag.id))

            results = (await session.scalars(query))
            total = (await session.scalar(query_count)) or 0

            return PaginatedResult(
                total=total,
                records=list(results),
                offset=offset,
                limit=limit
            )
        
    @classmethod
    async def get_tags_except_recipe_tags(cls, offset: int, limit:int, recipe_id:int):
        async with async_session() as session:
            subquery = (
                select(Tag.id)
                    .select_from(Recipe)
                    .where(Recipe.id == recipe_id)
            )
            query = (
                select(Tag)
                    .where(Tag.id.in_(subquery))
                    .order_by(Tag.name)
                    .offset(offset)
                    .limit(limit)
            )
            query_count = select(func.count(Tag.id))

            results = (await session.scalars(query))
            total = (await session.scalar(query_count)) or 0

            return PaginatedResult(
                total=total,
                records=list(results),
                offset=offset,
                limit=limit
            )