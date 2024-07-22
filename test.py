

import asyncio
from typing import List

from sqlalchemy import asc, desc, select
from sqlalchemy.orm import joinedload, lazyload, selectinload, subqueryload, contains_eager
from app.keyboards.base import InlineKeyboardBase, ReplyKeyboardBase
from app.models.enum import IngredientAmountTypeEnum
from app.models.recipe import Ingredient, Recipe, RecipeStep, Tag
from app.models.base import async_create_tables, async_drop_tables, async_session
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from app.translations import MessageTranslations


async def test():
    async with async_session() as session:
        query = (
            select(Recipe)
                .options(contains_eager(Recipe.steps), contains_eager(Recipe.tags))
                .filter(Recipe.id == 1)
                # .execution_options(populate_existing=True)
                .order_by(asc(RecipeStep.sequence_number), asc(Tag.id))
        )

        recipe = await session.scalar(query)
        print('steps')
        for step in recipe.steps:

            print(step.id)
        print('tags')
        for tag in recipe.tags:

            print(tag.id)


async def main():
    await async_create_tables()

    # await test()
    
    # await async_drop_tables()

# asyncio.run(main())

# amount_type_string = IngredientAmountTypeEnum(1).)

# print(amount_type_string)

print(IngredientAmountTypeEnum.get_from_annotation('Литры'))