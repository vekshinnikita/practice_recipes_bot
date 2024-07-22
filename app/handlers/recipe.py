from cgitb import text
from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import ContentType

from app.filters.admin import AdminFilter
from app.handlers.admin_update_recipe import AdminEditRecipe
from app.keyboards.base import InlineKeyboardBase
from app.keyboards.main_menu import MainMenuReplyKeyboard
from app.keyboards.pagination import PaginationInlineKeyboard
from app.keyboards.recipe import EditRecipeReplyKeyboard
from app.repository.recipe import RecipeRepo
from app.service.recipe import RecipeService
from app.service.tag import CATEGORY_BUTTONS, TagService
from app.translations import ButtonTranslations, MessageTranslations
from app.utils import replace_by_dict


router = Router(name='recipe')

class SearchState(StatesGroup):
    SEARCH_BY_Q = State()
    SEARCH_BY_CATEGORY = State()
    VIEW_RESULTS = State()
    VIEW_RECIPE_STEP = State()


async def start_search_recipe(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    q = data.get('q', None)
    category = data.get('category', None)
    is_random = data.get('is_random', False)

    reply_message_html, image_id, keyboard = await RecipeService.search_recipe_by_one(
        state=state,
        is_random=is_random,
        q=q,
        category=category,
        offset=0,
        is_admin=is_admin,
    )

    if not image_id:
        await state.clear()
        return await message.answer(
            text=reply_message_html,
            reply_markup=keyboard
        )
    else:
        await message.answer_photo(
            caption=reply_message_html,
            parse_mode=ParseMode.HTML,
            photo=image_id,
            reply_markup=keyboard
        )
        new_state = SearchState.VIEW_RESULTS
    await state.set_state(SearchState.VIEW_RESULTS)
    await state.update_data(is_admin=is_admin)

@router.message(F.text == ButtonTranslations.RANDOM_RECIPE)
async def random_recipe(message: types.Message, state: FSMContext, is_admin: bool):
    await state.set_data({
            'is_random': True
        })
    return await start_search_recipe(message, state, is_admin)

@router.message(SearchState.SEARCH_BY_Q, F.text)
@router.message(F.text == ButtonTranslations.SEARCH_RECIPE_BY_Q)
async def search_recipe_by_q(message: types.Message, state: FSMContext, is_admin: bool):
    if (await state.get_state()) == SearchState.SEARCH_BY_Q:
        await state.set_data({
            'q': message.text
        })
        return await start_search_recipe(message, state, is_admin)
    
    await message.answer(
        MessageTranslations.RECIPE_SEARCH,
        reply_markup=MainMenuReplyKeyboard(is_admin=is_admin)
    )
    await state.set_state(SearchState.SEARCH_BY_Q)

@router.message(SearchState.SEARCH_BY_CATEGORY, F.text)
@router.message(F.text.in_(CATEGORY_BUTTONS))
async def search_recipe_by_category(message: types.Message, state: FSMContext, is_admin: bool):
    if message.text not in CATEGORY_BUTTONS:
        await state.set_data({
            'category': message.text
        })
        await message.answer(
            text=MessageTranslations.SELECTED_CATEGORY,
            reply_markup=MainMenuReplyKeyboard(is_admin=is_admin)
        )
        return await start_search_recipe(message, state, is_admin)

    data = await state.get_data()
    new_data = {}
    offset = TagService.get_offset_tags(data.get('offset', 0)) 
    new_data['offset'] = offset
    
    is_show_more = message.text != ButtonTranslations.SEARCH_RECIPE_BY_CATEGORY
    keyboard = await RecipeService.get_tags_keyboard(
        limit=10,
        offset=offset,
    )

    reply_message = MessageTranslations.SHOW_MORE_CATEGORY if is_show_more else MessageTranslations.RECIPE_SEARCH_BY_CATEGORY

    await message.answer(
        reply_message,
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )
    await state.set_state(SearchState.SEARCH_BY_CATEGORY)


@router.callback_query(F.data.in_(['select','next', 'previous']), SearchState.VIEW_RESULTS)
async def search_recipes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data == 'select':
        await state.set_state(SearchState.VIEW_RECIPE_STEP)
        return await view_recipe_step(callback, state) ## TODO

    q = data.get('q', None)
    category = data.get('category', None)
    is_random = data.get('is_random', False)
    offset = data.get('offset', 0)
    is_admin = data.get('is_admin', False)
    
    if callback.data == 'next':
        offset += 1
    else:
        offset -= 1

    reply_message_html, image_id, keyboard = await RecipeService.search_recipe_by_one(
        state=state,
        q=q,
        is_random=is_random,
        category=category,
        offset=offset,
        is_admin=is_admin
    )

    new_photo = types.InputMediaPhoto(
        media=image_id, 
        caption=reply_message_html,
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()
    await callback.message.edit_media( #type: ignore
        media=new_photo,
        reply_markup=keyboard #type: ignore
    )

@router.callback_query(F.data.in_(['edit']), SearchState.VIEW_RESULTS, AdminFilter())
async def edit_recipe(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminEditRecipe.EDIT_RECIPE)
    await callback.message.answer( # type: ignore
        text=ButtonTranslations.ADMIN_EDIT_RECIPE,
        reply_markup=EditRecipeReplyKeyboard()
    )

@router.callback_query(F.data.in_(['next', 'previous']), SearchState.VIEW_RECIPE_STEP)
async def view_recipe_step(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    is_admin = data.get('is_admin', False)
    new_data = {}

    recipe_id = data.get('recipe_id', 0)

    last_step_index = data.get('last_step_index', None) 
    if last_step_index is None:
        last_step_index = await RecipeService.get_last_recipe_step_index(recipe_id) or 0
        new_data['last_step_index'] = last_step_index 

    current_step_index = data.get('current_step_index', 1)
    if callback.data == 'next':
        current_step_index += 1
    elif callback.data == 'previous':
        current_step_index -= 1
    new_data['current_step_index'] = current_step_index

    message, keyboard, image_id = await RecipeService.get_recipe_step(recipe_id, current_step_index, last_step_index)
    await callback.answer()

    if image_id is None and message is None and keyboard is None:
        await callback.message.answer( #type: ignore
            text=MessageTranslations.RECIPE_STEP_NOT_FOUND,
            keyboard=MainMenuReplyKeyboard(is_admin=is_admin)
        )
        await state.clear()
        return 
    elif callback.data == 'select':
        await callback.message.answer_photo( #type: ignore
            caption=message,
            photo=image_id, #type: ignore
            reply_markup=keyboard
        )
    else:
        new_photo = types.InputMediaPhoto(
            media=image_id, #type: ignore
            caption=message,
        )
        await callback.message.edit_media( #type: ignore
            media=new_photo,
            reply_markup=keyboard
        )

    await state.update_data(**new_data)


@router.callback_query(F.data.in_(['done']), SearchState.VIEW_RECIPE_STEP)
async def done_recipe(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    is_admin = data.get('is_admin', False)
    await state.clear()
    await callback.message.answer(# type: ignore
        text=MessageTranslations.RECIPE_DONE,
        keyboard=MainMenuReplyKeyboard(is_admin=is_admin)
    )


# @router.message(F.photo)
# async def get_photo_id(message: types.Message):
#     photo_id = message.photo[-1].file_id # type: ignore
#     await message.answer(text=photo_id)

@router.message(F.sticker)
async def sticker(message: types.Message):
    photo_id = message.photo[-1].file_id # type: ignore
    await message.answer(text=photo_id)