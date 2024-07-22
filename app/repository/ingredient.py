from typing import List
from sqlalchemy import func, select
from app.models.recipe import Admin, Ingredient, Recipe, RecipeIngredient, Tag
from app.models.base import async_session
from app.types.pagination import PaginatedResult

class IngredientRepo:

    @classmethod
    async def add_ingredient(cls, name: str):
        async with async_session() as session:
            ingredient = Ingredient(name=name)
            session.add(ingredient)
            await session.commit()

    @classmethod
    async def get_ingredients_by_ids(cls, ids: List[int]) -> List[Ingredient] :
        if not ids:
            return []
        
        async with async_session() as session:
            query = (
                select(Ingredient)
                .filter(
                    Ingredient.id.in_(ids)
                )
            )

            return list(await session.scalars(query))

    @classmethod
    async def get_ingredient_by_name(cls, name: str):
        async with async_session() as session:
            query = (
                select(Ingredient)
                .filter(
                    Ingredient.name == name
                )
            )

            return await session.scalar(query)

    @classmethod
    async def get_ingredients(cls, offset: int, limit:int):
        async with async_session() as session:
            query = (
                select(Ingredient)
                .order_by(Ingredient.name)
                .offset(offset)
                .limit(limit)
            )
            query_count = select(func.count(Ingredient.id))

            results = (await session.scalars(query))
            total = (await session.scalar(query_count)) or 0

            return PaginatedResult(
                total=total,
                records=list(results),
                offset=offset,
                limit=limit
            )
        
    @classmethod
    async def get_ingredients_not_in_recipe(cls, offset: int, limit:int, recipe_id:int):
        async with async_session() as session:
            subquery = (
                select(RecipeIngredient.ingredient_id)
                    .where(RecipeIngredient.recipe_id == recipe_id)
            )
            query = (
                select(Ingredient)
                    .where(Ingredient.id.not_in(subquery))
                    .order_by(Ingredient.name)
                    .offset(offset)
                    .limit(limit)
            )
            query_count = select(func.count(Ingredient.id))

            results = (await session.scalars(query))
            total = (await session.scalar(query_count)) or 0

            return PaginatedResult(
                total=total,
                records=list(results),
                offset=offset,
                limit=limit
            )
