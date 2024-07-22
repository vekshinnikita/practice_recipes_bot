

from typing import Literal

from app.translations import ButtonTranslations
from .base import InlineKeyboardBase
from aiogram.types import  InlineKeyboardButton

left_button = InlineKeyboardButton(
    text='Предыдущий',
    callback_data='previous'
)

right_button = InlineKeyboardButton(
    text='Следующий',
    callback_data='next'
)

class PaginationInlineKeyboard(InlineKeyboardBase):
    
    def __new__(cls, direction: Literal['only_prev', 'only_next', 'both', 'none'] = 'both', **kwargs):
        if direction == 'both':
            cls.inline_keyboard = [[left_button, right_button]]
        elif direction == 'only_prev':
            cls.inline_keyboard = [[left_button]]
        elif direction == 'only_next':
            cls.inline_keyboard = [[right_button]]
        else:
            return None
        
        return super().__new__(cls, **kwargs)
        