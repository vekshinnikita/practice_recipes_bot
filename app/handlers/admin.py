from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.filters.admin import AdminFilter
from app.keyboards.admin import AdminPanelReplyKeyboard
from app.keyboards.base import ReplyKeyboardBase
from app.keyboards.main_menu import MainMenuReplyKeyboard
from app.models.recipe import Ingredient
from app.service.admin import AdminService
from app.service.ingredient import IngredientService
from app.service.tag import TagService
from app.translations import ButtonTranslations, MessageTranslations


router = Router(name='admin')

admin_password="password"

class AdminState(StatesGroup):
    TYPING_PASSWORD = State()
    ADD_TAG = State()
    ADD_INGREDIENT = State()


@router.message(Command("admin"))
async def cmd_start(message: types.Message, is_admin: bool):
    if(is_admin):
        await message.answer(
            'Вы админ', 
            reply_markup = MainMenuReplyKeyboard(is_admin=is_admin)
        )
    else:
        await message.answer(
            'Вы не админ', 
            reply_markup = MainMenuReplyKeyboard(is_admin=is_admin)
        )


@router.message(Command("set_admin"), ~AdminFilter())
async def request_password(message: types.Message, state: FSMContext):
    await state.set_state(AdminState.TYPING_PASSWORD)
    await message.answer(
        text=MessageTranslations.ADMIN_SET
    )


@router.message(AdminState.TYPING_PASSWORD, F.text)
async def set_admin(message: types.Message, state: FSMContext, is_admin: bool):
    if message.text == admin_password:
        msg = MessageTranslations.ADMIN_SET_SUCCESS
        if message.from_user:
            await AdminService.set_admin(message.from_user.id)
        is_admin = True
    else:
        msg = MessageTranslations.ADMIN_SET_WRONG_PASSWORD

    await message.answer(
        text=msg,
        keyboard=MainMenuReplyKeyboard(is_admin=is_admin)
    )
    await state.clear()


@router.message(F.text == ButtonTranslations.ADMIN_PANEL, AdminFilter())
async def admin_panel(message: types.Message, state: FSMContext):
    await message.answer(
        text=MessageTranslations.ADMIN_PANEL_GREETING,
        reply_markup=AdminPanelReplyKeyboard()
    )


@router.message(F.text == ButtonTranslations.ADMIN_ADD_TAG, AdminFilter())
async def request_tag_name(message: types.Message, state: FSMContext):
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_TAG,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AdminState.ADD_TAG)
    

@router.message(AdminState.ADD_TAG, F.text, AdminFilter())
async def add_tag(message: types.Message, state: FSMContext):
    name = message.text or ''
    await TagService.add_tag(name)
    
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_TAG_SUCCESS,
        reply_markup=AdminPanelReplyKeyboard()
    )
    await state.clear()


@router.message(F.text == ButtonTranslations.ADMIN_ADD_INGREDIENT, AdminFilter())
async def request_ingredient_name(message: types.Message, state: FSMContext):
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_INGREDIENT,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AdminState.ADD_INGREDIENT)


@router.message(AdminState.ADD_INGREDIENT, F.text, AdminFilter())
async def add_ingredient(message: types.Message, state: FSMContext):
    name = message.text or ''
    await IngredientService.add_ingredient(name)
    
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_INGREDIENT_SUCCESS,
        reply_markup=AdminPanelReplyKeyboard()
    )
    await state.clear()
