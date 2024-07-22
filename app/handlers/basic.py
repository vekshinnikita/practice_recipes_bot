from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from app.keyboards.admin import AdminPanelReplyKeyboard
from app.keyboards.main_menu import MainMenuReplyKeyboard
from app.translations import ButtonTranslations, MessageTranslations


router = Router(name='basic')


@router.message(Command("start"))
async def cmd_start(message: types.Message, is_admin: bool):
    
    await message.answer(
        MessageTranslations.START, 
        reply_markup = MainMenuReplyKeyboard(is_admin=is_admin)
    )

@router.message(F.text == ButtonTranslations.MAIN_MENU)
async def main_menu(message: types.Message, state: FSMContext, is_admin: bool):
    await state.clear()
    await message.answer(
        ButtonTranslations.MAIN_MENU, 
        reply_markup = MainMenuReplyKeyboard(is_admin=is_admin)
    )

@router.message(F.text == ButtonTranslations.CANCEL)
async def cancel_admin(message: types.Message, state: FSMContext, is_admin: bool):
    await state.clear()
    await message.answer(
        ButtonTranslations.MAIN_MENU, 
        reply_markup = MainMenuReplyKeyboard(is_admin=is_admin)
    )
