

from typing import List

from app.translations import ButtonTranslations
from .base import ReplyKeyboardBase
from aiogram.types import KeyboardButton


class MainMenuReplyKeyboard(ReplyKeyboardBase):

    resize_keyboard=True
    keyboard = [
        [KeyboardButton(text=ButtonTranslations.SEARCH_RECIPE_BY_CATEGORY), KeyboardButton(text=ButtonTranslations.SEARCH_RECIPE_BY_Q)],
        [KeyboardButton(text=ButtonTranslations.RANDOM_RECIPE)],
    ]

    @classmethod
    def get_admin_keyboard(cls) -> List[List[KeyboardButton]]:
        keyboard = [*cls.keyboard, [KeyboardButton(text=ButtonTranslations.ADMIN_PANEL)]]
        return keyboard
    

