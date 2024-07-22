

from app.keyboards.base import InlineKeyboardBase, ReplyKeyboardBase
from aiogram.types import InlineKeyboardButton, KeyboardButton

from app.translations import ButtonTranslations


class SelectRecipeInlineKeyboard(InlineKeyboardBase):

    inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Выбрать', 
                callback_data='select'
            )
        ]
    ]


class DoneRecipeInlineKeyboard(InlineKeyboardBase):

    inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Готово', 
                callback_data='done'
            )
        ]
    ]


class CancelReplyKeyboard(ReplyKeyboardBase):

    resize_keyboard=True
    keyboard=[
        [
            KeyboardButton(
                text=ButtonTranslations.CANCEL
            )
        ]
    ]

class EditRecipeInlineKeyboard(InlineKeyboardBase):

    @classmethod
    def get_admin_keyboard(cls):
        return [
            [InlineKeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE,
                callback_data='edit'
            )]
        ]

class EditRecipeReplyKeyboard(ReplyKeyboardBase):

    resize_keyboard=True
    keyboard=[
        [
            KeyboardButton(
                text=ButtonTranslations.MAIN_MENU
            ),
        ],
        [
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_NAME
            ),
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_DESCRIPTION
            ),
        ],
        [
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_IMAGE
            ),
        ],
        [
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_DELETE_TAG
            ),
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_TAG
            ),
        ],
        [
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_DELETE_INGREDIENT
            ),
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_INGREDIENT
            ),
        ],
        [
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_DELETE_STEP
            ),
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_STEP
            ),
        ],
        [
            KeyboardButton(
                text=ButtonTranslations.ADMIN_EDIT_RECIPE_CHANGE_STEP_INDEXES
            ),
        ],
        [
            KeyboardButton(
                text=ButtonTranslations.ADMIN_DELETE_RECIPE
            ),
            
        ]
    ]

class ConfirmDeleteReplyKeyboard(ReplyKeyboardBase):
    resize_keyboard=True
    
    keyboard = [
        [
           KeyboardButton(
                text=ButtonTranslations.YES
            ),
            KeyboardButton(
                text=ButtonTranslations.NO
            ), 
        ]
    ]