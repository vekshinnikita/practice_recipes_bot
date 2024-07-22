

from typing import List
from app.models.recipe import Tag
from app.repository.tag import TagRepo
from app.translations import ButtonTranslations
from app.types.pagination import PaginatedResult

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


CATEGORY_BUTTONS = [
    ButtonTranslations.SEARCH_RECIPE_BY_CATEGORY,
    ButtonTranslations.PREV,
    ButtonTranslations.NEXT
]

tag_list_manage_buttons = [ButtonTranslations.NEXT, ButtonTranslations.PREV, ButtonTranslations.DONE]

class TagService:

    @classmethod
    async def add_tag(cls, tag_name: str):
        await TagRepo.add_tag(name=tag_name)

    @classmethod
    async def get_tag_by_name(cls, name: str):
        return await TagRepo.get_tag_by_name(name=name)

    @classmethod
    def get_offset_tags(cls, text, offset: int=0):
        if text == ButtonTranslations.NEXT:
            offset += 1
        elif text == ButtonTranslations.PREV:
            offset -= 1
        
        return offset

    @classmethod
    def _generate_tags_keyboard(cls, paginated_tags: PaginatedResult[Tag], keyboard_builder: ReplyKeyboardBuilder | None):
        keyboard = keyboard_builder if keyboard_builder else ReplyKeyboardBuilder()

        left_adjust = []
        right_adjust = []

        if paginated_tags.is_previous():
            left_adjust.append(1)
            keyboard.button(text=ButtonTranslations.PREV)

        for tag in paginated_tags.records:
            keyboard.button(text=tag.name)

        if paginated_tags.is_next():
            right_adjust.append(1)
            keyboard.button(text=ButtonTranslations.NEXT)

        adjust = [2] * (paginated_tags.len()//2)
        if paginated_tags.len() % 2 == 1:
            adjust += [1]

        keyboard.adjust(*(left_adjust + adjust + right_adjust))
        return keyboard

    @classmethod
    async def get_tags_keyboard(cls, keyboard_builder: ReplyKeyboardBuilder | None = None, offset:int = 0, limit: int=10) -> ReplyKeyboardBuilder:
        tags = await TagRepo.get_tags(offset=offset, limit=limit)
        keyboard = cls._generate_tags_keyboard(tags, keyboard_builder)

        return keyboard
    
    @classmethod
    async def get_tags_not_in_recipe_keyboard(
        cls, 
        recipe_id: int,
        keyboard_builder: ReplyKeyboardBuilder | None = None, 
        offset:int = 0, 
        limit: int=10
    ) -> ReplyKeyboardBuilder:
        tags = await TagRepo.get_tags_except_recipe_tags(
            offset=offset, 
            limit=limit,
            recipe_id=recipe_id
        )
        keyboard = cls._generate_tags_keyboard(tags, keyboard_builder)

        return keyboard


        