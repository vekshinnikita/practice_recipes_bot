from asyncio import Condition
from sqlalchemy import Integer, Subquery, bindparam, delete, desc, insert, or_, select, update
from sqlalchemy.sql import func
from sqlalchemy.orm import selectinload, contains_eager, joinedload

from app.types.pagination import PaginatedResult
from app.models.recipe import Ingredient, Recipe, RecipeIngredient, RecipeStep, RecipeTag, Tag
from app.models.base import async_session


class RecipeRepo:

    @classmethod
    async def search_paginated_recipes(
        cls, 
        q: str | None, 
        category: str | None,
        limit: int = 10, 
        offset: int = 0
    ) -> PaginatedResult[Recipe]:
        conditions = []

        if q:
            search_terms = q.split()
            search_pattern = '|'.join(search_terms)
            conditions.append(Recipe.nocase_name.op('regexp')(search_pattern))
        
        if category:
            conditions.append(Tag.name == category)

        async with async_session() as session:
            query = (
                    select(Recipe)
                        .distinct()
                        .join(Recipe.tags, isouter=True)
                        .filter(
                            *conditions
                        )
                        .options(
                            selectinload(Recipe.tags),
                            selectinload(Recipe.ingredients).joinedload(RecipeIngredient.ingredient)
                        )
                        .order_by(Recipe.name)
                        .offset(offset)
                        .limit(limit)
            )

            query_count = (
                select(func.count(Recipe.id.distinct()).label('total_count'))
                    .join(Recipe.tags, isouter=True)
                    .filter(*conditions)
            )
            
            results = (await session.execute(query)).unique().scalars().all()
            total = (await session.execute(query_count)).scalar() or 0

            return PaginatedResult(
                total=total,
                records=list(results),
                offset=offset,
                limit=limit
            )
        
    @classmethod
    async def get_random_recipe(cls) -> Recipe:
        async with async_session() as session:
            query = (
                select(Recipe)
                    .join(Recipe.tags, isouter=True)
                    .options(
                        selectinload(Recipe.tags),
                        selectinload(Recipe.ingredients).joinedload(RecipeIngredient.ingredient)
                    )
                    .order_by(func.random())
                    .limit(1)
            )


            return await session.scalar(query) #type: ignore
        
        
    @classmethod
    async def get_recipe_step(cls, recipe_id: int, step_index):
        async with async_session() as session:
            query = (
                select(RecipeStep)
                .filter(
                    RecipeStep.recipe_id == recipe_id,
                    RecipeStep.sequence_number == step_index
                )
            )

            return await session.scalar(query)
        
    @classmethod
    async def get_last_recipe_step_index(cls, recipe_id):
        async with async_session() as session:
            query = (
                select(RecipeStep.sequence_number)
                .filter(
                    RecipeStep.recipe_id == recipe_id,
                )
                .order_by(RecipeStep.sequence_number.desc())
                .limit(1)
            )

            return await session.scalar(query) 
        
    @classmethod
    async def add_recipe_from_model(cls, recipe: Recipe):
        async with async_session() as session:
            session.add(recipe)
            await session.commit()

    @classmethod
    async def add_tag_to_recipe(cls, recipe_id, tag_id):
        async with async_session() as session:
            recipe_tag = RecipeTag(
                recipe_id=recipe_id,
                tag_id=tag_id
            )
            session.add(recipe_tag)
            await session.commit()

    @classmethod
    async def update_recipe(cls, recipe_id, **kwargs):
        name: str = kwargs.get('name', None)
        if name:
            kwargs['nocase_name'] = name.lower()
            
        async with async_session() as session:
            
            stmt = (
                update(Recipe)
                    .where(Recipe.id == recipe_id)
                    .values(**kwargs)
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def add_ingredient_to_recipe(cls, recipe_id: int, new_ingredient: dict):
        async with async_session() as session:
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe_id,
                ingredient_id=new_ingredient.get('ingredient_id', 0),
                amount_type=new_ingredient.get('amount_type', 'LITTER'),
                amount=new_ingredient.get('amount', 0)
            )

            session.add(recipe_ingredient)
            await session.commit()

    @classmethod
    async def add_step_to_recipe(cls, recipe_id: int, new_step: dict):
        async with async_session() as session:
            query = (
                select(func.max(RecipeStep.sequence_number))
                    .where(RecipeStep.recipe_id == recipe_id)
            ) 
            max = (await session.scalar(query)) or 0
            sequence_number = max+ 1
            
            step = RecipeStep(
                recipe_id=recipe_id,
                description=new_step.get('description', ''),
                image_id=new_step.get('image_id', ''),
                sequence_number=sequence_number
            )
            session.add(step)
            await session.commit()

    @classmethod
    async def get_recipe_steps(cls, recipe_id:int):
        async with async_session() as session:
            query = (
                select(RecipeStep)
                    .where(RecipeStep.recipe_id==recipe_id)
                    .order_by(RecipeStep.sequence_number)
            )

            return list(await session.scalars(query))

    @classmethod 
    async def change_steps_indexes(cls, recipe_id: int, changed_indexes_dict: dict[int,int]):
        async with async_session() as session:

            old_indexes = [key for key, value in changed_indexes_dict.items()]

            subquery = (
                 select(RecipeStep)
                    .where(
                        RecipeStep.recipe_id == recipe_id, 
                        RecipeStep.sequence_number.in_(old_indexes),
                    )
            )

            recipe_steps = list(await session.scalars(subquery))

            for step in recipe_steps:
                step.sequence_number = changed_indexes_dict[step.sequence_number]
                session.add(step)

            await session.commit()


    @classmethod
    async def delete_recipe_by_id(cls, recipe_id: int):
        async with async_session() as session:
            stmt = (
                delete(Recipe)
                    .where(Recipe.id == recipe_id)
            )

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_recipe_tags(cls, recipe_id: int):
        async with async_session() as session:
            query = (
                select(Tag)
                    .join(RecipeTag)
                    .where(RecipeTag.recipe_id == recipe_id)
            )

            return list(await session.scalars(query))
        
    @classmethod
    async def get_recipe_ingredients(cls, recipe_id: int):
        async with async_session() as session:
            query = (
                select(Ingredient)
                    .join(RecipeIngredient)
                    .where(RecipeIngredient.recipe_id == recipe_id)
            )

            return list(await session.scalars(query))

    @classmethod
    async def delete_recipe_tag_by_id(cls, recipe_id: int, tag_id:int):
        async with async_session() as session:
            stmt = (
                delete(RecipeTag)
                    .where(
                        RecipeTag.recipe_id == recipe_id,
                        RecipeTag.tag_id == tag_id
                    )
            )

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_recipe_ingredient_by_id(cls, recipe_id: int, ingredient_id: int):
        async with async_session() as session:
            stmt = (
                delete(RecipeIngredient)
                    .where(
                        RecipeIngredient.recipe_id == recipe_id,
                        RecipeIngredient.ingredient_id == ingredient_id
                    )
            )

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_recipe_step_by_index(cls, recipe_id: int, step_index: int):
        async with async_session() as session:
            stmt = (
                delete(RecipeStep)
                    .where(
                        RecipeStep.recipe_id == recipe_id,
                        RecipeStep.sequence_number == step_index
                    )
            )

            await session.execute(stmt)
            await session.commit()