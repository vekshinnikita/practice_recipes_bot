

from typing import List
from app.models.enum import IngredientAmountTypeEnum
from app.models.recipe import Ingredient, RecipeIngredient, Tag
from app.repository.ingredient import IngredientRepo
from app.translations import ButtonTranslations
from app.types.pagination import PaginatedResult
from aiogram.utils.keyboard import ReplyKeyboardBuilder

tag_list_manage_buttons = [ButtonTranslations.NEXT, ButtonTranslations.PREV]

class IngredientService:

    @classmethod
    async def add_ingredient(cls, ingredient_name: str):
        await IngredientRepo.add_ingredient(name=ingredient_name)

    @classmethod
    async def get_ingredient_by_name(cls, name: str):
        return await IngredientRepo.get_ingredient_by_name(name=name)

    @classmethod
    def get_offset_ingredients(cls, text, offset: int=0):
        if text == ButtonTranslations.NEXT:
            offset += 1
        elif text == ButtonTranslations.PREV:
            offset -= 1
        
        return offset

    @classmethod
    def generate_ingredients_keyboard(cls, paginated_ingredients: PaginatedResult[Ingredient], keyboard_builder: ReplyKeyboardBuilder | None):
        keyboard = keyboard_builder if keyboard_builder else ReplyKeyboardBuilder()

        left_adjust = []
        right_adjust = []

        if paginated_ingredients.is_previous():
            left_adjust.append(1)
            keyboard.button(text=ButtonTranslations.PREV)

        for tag in paginated_ingredients.records:
            keyboard.button(text=tag.name)

        if paginated_ingredients.is_next():
            right_adjust.append(1)
            keyboard.button(text=ButtonTranslations.NEXT)

        adjust = [2] * (paginated_ingredients.len()//2)
        if paginated_ingredients.len() % 2 == 1:
            adjust += [1]

        keyboard.adjust(*(left_adjust + adjust + right_adjust))
        return keyboard

    @classmethod
    async def get_ingredients_keyboard(cls, keyboard_builder: ReplyKeyboardBuilder | None = None, offset:int = 0, limit: int=10) -> ReplyKeyboardBuilder:
        ingredients = await IngredientRepo.get_ingredients(offset=offset, limit=limit)
        keyboard = cls.generate_ingredients_keyboard(ingredients, keyboard_builder)

        return keyboard
    
    @classmethod
    async def get_ingredients_not_in_recipe_keyboard(
        cls, 
        recipe_id:int,
        keyboard_builder: ReplyKeyboardBuilder | None = None, 
        offset:int = 0, 
        limit: int=10,
    ):
        ingredients = await IngredientRepo.get_ingredients_not_in_recipe(offset=offset, limit=limit, recipe_id=recipe_id)
        if not ingredients.len():
            return None
        keyboard = cls.generate_ingredients_keyboard(ingredients, keyboard_builder)
        
        return keyboard
    
    @classmethod
    def get_ingredient_amount_types_keyboard(cls):        
        amount_types: List[str] = [
            ingredient.get_full_annotation() 
            for ingredient in IngredientAmountTypeEnum
        ]
        
        keyboard = ReplyKeyboardBuilder()
        for amount_type in amount_types:
            keyboard.button(text=amount_type)
        keyboard.adjust(2)

        return keyboard