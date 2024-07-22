
from typing import List
from app.translations import ButtonTranslations
from aiogram.types import KeyboardButton

from app.keyboards.base import ReplyKeyboardBase


class AdminPanelReplyKeyboard(ReplyKeyboardBase):

    resize_keyboard=True
    keyboard = [
        [KeyboardButton(text=ButtonTranslations.MAIN_MENU)],
        [KeyboardButton(text=ButtonTranslations.ADMIN_ADD_TAG), KeyboardButton(text=ButtonTranslations.ADMIN_ADD_INGREDIENT)],
        [KeyboardButton(text=ButtonTranslations.ADMIN_ADD_RECIPE)],
    ]

    @classmethod
    def get_admin_keyboard(cls) -> List[List[KeyboardButton]]:
        return cls.keyboard
    

class AdminAddMoreStepReplyKeyboard(ReplyKeyboardBase):

    resize_keyboard=True
    keyboard = [
        [KeyboardButton(text=ButtonTranslations.ADMIN_ADD_STEP_MORE)],
        [KeyboardButton(text=ButtonTranslations.DONE)],
    ]
