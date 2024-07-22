from turtle import right
from typing import List
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.keyboards.base import CombineInlineKeyboards, InlineKeyboardBase, ReplyKeyboardBase
from app.keyboards.pagination import PaginationInlineKeyboard
from app.keyboards.recipe import DoneRecipeInlineKeyboard, EditRecipeInlineKeyboard, SelectRecipeInlineKeyboard
from app.models.enum import IngredientAmountTypeEnum
from app.models.recipe import Ingredient, Recipe, RecipeIngredient, RecipeStep, Tag
from app.repository.ingredient import IngredientRepo
from app.repository.tag import TagRepo
from app.service.ingredient import IngredientService
from app.service.tag import TagService
from app.types.keyboard import AnyKeyboard
from app.types.pagination import PaginatedResult
from app.repository.recipe import RecipeRepo
from app.translations import ButtonTranslations, MessageTranslations
from app.utils import get_pagination_direction, replace_by_dict


class RecipeService:

    @classmethod
    def _generate_ingredient_list(cls, ingredients: List[RecipeIngredient]):
        ingredient_list = []
        for i in ingredients:
            amount_type_string = IngredientAmountTypeEnum(i.amount_type).get_short_annotation()
            string = f'{i.ingredient.name}: {i.amount} {amount_type_string}'
            ingredient_list.append(f'\t\t\t\t- {string}')

        return '\n'.join(ingredient_list)

    @classmethod
    def _generate_category_list(cls, tags: List[Tag]):
        category_list = []
        for tag in tags:
            category_list.append(tag.name)

        return ', '.join(category_list)
    
    @classmethod
    def _get_search_message(cls, recipe: Recipe):
        ingredient_list = cls._generate_ingredient_list(recipe.ingredients)
        category_list = cls._generate_category_list(recipe.tags)
        
        replace_dict = {
            'title': recipe.name,
            'description': recipe.description,
            'ingredient_list': ingredient_list,
            'category_list': category_list or ' - '
        }
        return replace_by_dict(MessageTranslations.RECIPE_SEARCH_VIEW_RESULT_HTML, replace_dict)
    
    @classmethod
    async def _update_search_recipe_state(cls, state: FSMContext, q: str | None, offset:int, recipe_id: int):
        new_data = {
            'offset': offset,
            'q': q
        }
        if recipe_id:
            new_data['recipe_id'] = recipe_id

        await state.update_data(**new_data)

    @classmethod
    async def _search_paginated_recipes(
        cls, 
        is_random: bool,
        q: str | None, 
        category: str | None,
        offset:int = 0, 
    ):
        if is_random:
            recipe = await RecipeRepo.get_random_recipe()
            return PaginatedResult(
                total=1,
                records=[recipe],
                offset=0,
                limit=1
            )
        
        return await RecipeRepo.search_paginated_recipes(
            q=q,
            category=category,
            limit=1,
            offset=offset
        )

    @classmethod
    async def search_recipe_by_one(
        cls, 
        state: FSMContext, 
        is_random: bool,
        q: str | None, 
        category: str | None,
        offset:int = 0, 
        is_admin: bool = False
    ) -> tuple[str, str, AnyKeyboard]:
        paginated_result = await cls._search_paginated_recipes(
            is_random=is_random,
            q=q,
            category=category,
            offset=offset,
        )
        
        if paginated_result.len() == 0:
            return MessageTranslations.RECIPE_SEARCH_NOT_FOUND, '', None
        
        recipe = paginated_result.records[0]

        await cls._update_search_recipe_state(
            state=state,
            q=q,
            offset=offset,
            recipe_id=recipe.id
        )
        
        reply_message = cls._get_search_message(recipe)
        keyboard = CombineInlineKeyboards(
            SelectRecipeInlineKeyboard(),
            EditRecipeInlineKeyboard(is_admin=is_admin),
            PaginationInlineKeyboard(
                direction=paginated_result.get_direction(),
                
            )
        )
        
        return (
            reply_message, 
            recipe.image_id, 
            keyboard
        )
        
    @classmethod
    async def get_recipe_step(cls, recipe_id: int, step_index: int, last_step_index: int):
        recipe_step = await RecipeRepo.get_recipe_step(recipe_id, step_index)

        if not recipe_step:
            return None, None, None

        message = recipe_step.description
        direction = get_pagination_direction(1, last_step_index, step_index)
        
        keyboard = CombineInlineKeyboards(
            PaginationInlineKeyboard(
                direction=direction,
            ),
        )
        
        if direction == 'only_prev':
            keyboard = CombineInlineKeyboards(
                keyboard,
                DoneRecipeInlineKeyboard()
            )

        return (message, keyboard, recipe_step.image_id)

    @classmethod
    async def get_last_recipe_step_index(cls, recipe_id: int):
        return await RecipeRepo.get_last_recipe_step_index(recipe_id)


    @classmethod
    async def get_tags_keyboard(cls, offset:int = 0, limit: int=10):
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text=ButtonTranslations.MAIN_MENU)
        keyboard.adjust(1)

        return await TagService.get_tags_keyboard(
            offset=offset, 
            limit=limit,
            keyboard_builder=keyboard
        )
    
    @classmethod
    async def update_recipe(cls, recipe_id, **kwargs):
        await RecipeRepo.update_recipe(recipe_id, **kwargs)

    @classmethod
    async def add_tag_to_recipe(cls, recipe_id, tag_name):
        tag = await TagRepo.get_tag_by_name(name=tag_name)
        
        if not tag:
            return 
        
        await RecipeRepo.add_tag_to_recipe(
            recipe_id=recipe_id,
            tag_id=tag.id,
        )

    @classmethod
    async def add_ingredient_to_recipe(cls, recipe_id: int, new_ingredient: dict):
        await RecipeRepo.add_ingredient_to_recipe(recipe_id, new_ingredient)
        
    @classmethod
    async def add_step_to_recipe(cls, recipe_id:int, new_step: dict):
        await RecipeRepo.add_step_to_recipe(recipe_id=recipe_id, new_step=new_step)

    @classmethod
    def _generate_step_string(cls, step: RecipeStep):
        string = f'{step.sequence_number}: '
        short_step_description = f'{step.description[:20]}...' if len(step.description) > 20 else step.description

        return string + short_step_description

    @classmethod
    async def get_recipe_steps_message(cls, recipe_id:int):
        steps = await RecipeRepo.get_recipe_steps(recipe_id)
        if not steps:
            return None
        string_steps = [cls._generate_step_string(step) for step in steps]

        return ',\n\n'.join(string_steps)

    @classmethod
    async def change_steps_indexes(cls, recipe_id, indexes):

        changed_indexes_dict = {
            index+1: value_index
            for index, value_index in enumerate(indexes) if index+1 != value_index
        }

        await RecipeRepo.change_steps_indexes(recipe_id, changed_indexes_dict)

    @classmethod
    async def get_recipe_ingredients_keyboard(cls, recipe_id: int):

        ingredients = await RecipeRepo.get_recipe_ingredients(recipe_id=recipe_id)
        keyboard = ReplyKeyboardBuilder()

        for ingredient in ingredients:
            keyboard.button(text=ingredient.name)

        keyboard.adjust(2)
        return keyboard
    
    @classmethod
    async def get_recipe_tags_keyboard(cls, recipe_id: int):

        tags = await RecipeRepo.get_recipe_tags(recipe_id=recipe_id)
        keyboard = ReplyKeyboardBuilder()

        for tag in tags:
            keyboard.button(text=tag.name)

        keyboard.adjust(2)
        return keyboard
    
    @classmethod
    async def get_recipe_steps_keyboard(cls, recipe_id: int):

        steps = await RecipeRepo.get_recipe_steps(recipe_id=recipe_id)
        if not steps:
            return None

        keyboard = ReplyKeyboardBuilder()

        for step in steps:
            step_string = cls._generate_step_string(step)
            keyboard.button(text=step_string)

        keyboard.adjust(1)
        return keyboard

    @classmethod
    async def delete_recipe_tag_by_name(cls, recipe_id, tag_name):
        tag = await TagRepo.get_tag_by_name(tag_name)
        if not tag:
            return

        await RecipeRepo.delete_recipe_tag_by_id(
            recipe_id=recipe_id, 
            tag_id=tag.id
        )

    @classmethod
    async def delete_recipe_ingredient_by_name(cls, recipe_id, ingredient_name):
        ingredient = await IngredientRepo.get_ingredient_by_name(ingredient_name)
        if not ingredient:
            return

        await RecipeRepo.delete_recipe_ingredient_by_id(
            recipe_id=recipe_id, 
            ingredient_id=ingredient.id
        )

    @classmethod
    async def delete_recipe_step_by_index(cls, recipe_id, message: str):
        step_index = int(message.split(':')[0])

        await RecipeRepo.delete_recipe_step_by_index(
            recipe_id=recipe_id, 
            step_index=step_index
        )

    @classmethod
    async def delete_recipe(cls, recipe_id: int):
        await RecipeRepo.delete_recipe_by_id(
            recipe_id=recipe_id
        )