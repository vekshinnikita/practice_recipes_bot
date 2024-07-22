from curses.ascii import isdigit
from mailbox import Message
from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.filters.admin import AdminFilter
from app.service.tag import CATEGORY_BUTTONS
from app.keyboards.admin import AdminAddMoreStepReplyKeyboard, AdminPanelReplyKeyboard
from app.keyboards.base import ReplyKeyboardBase
from app.keyboards.main_menu import MainMenuReplyKeyboard
from app.keyboards.recipe import CancelReplyKeyboard, ConfirmDeleteReplyKeyboard, EditRecipeReplyKeyboard
from app.models.enum import IngredientAmountTypeEnum
from app.service.admin import AdminService
from app.service.admin_add_recipe import AdminAddRecipeService
from app.service.ingredient import IngredientService
from app.service.recipe import RecipeService
from app.service.tag import TagService, tag_list_manage_buttons
from app.translations import ButtonTranslations, MessageTranslations


router = Router(name='admin_update_recipe')

class AdminEditRecipe(StatesGroup):
    EDIT_RECIPE = State()

    EDIT_RECIPE_NAME = State()
    EDIT_RECIPE_DESCRIPTION = State()
    EDIT_RECIPE_IMAGE = State()
    
    EDIT_RECIPE_DELETE_TAG = State()
    EDIT_RECIPE_ADD_TAG = State()

    EDIT_RECIPE_DELETE_INGREDIENT = State()
    EDIT_RECIPE_ADD_INGREDIENT = State()
    EDIT_RECIPE_ADD_INGREDIENT_AMOUNT_TYPE = State()
    EDIT_RECIPE_ADD_INGREDIENT_AMOUNT = State()

    EDIT_RECIPE_DELETE_STEP  = State()
    EDIT_RECIPE_ADD_STEP_DESCRIPTION = State()
    EDIT_RECIPE_ADD_STEP_IMAGE = State()
    EDIT_RECIPE_CHANGE_INDEXES= State()

    DELETE_RECIPE = State()

ratio_buttons_and_message_dict = {
    ButtonTranslations.ADMIN_EDIT_RECIPE_NAME: MessageTranslations.ADMIN_UPDATE_RECIPE_NAME,
    ButtonTranslations.ADMIN_EDIT_RECIPE_DESCRIPTION: MessageTranslations.ADMIN_UPDATE_RECIPE_DESCRIPTION,
    ButtonTranslations.ADMIN_EDIT_RECIPE_IMAGE: MessageTranslations.ADMIN_UPDATE_RECIPE_IMAGE,
}

ratio_buttons_and_state_dict = {
    ButtonTranslations.ADMIN_EDIT_RECIPE_NAME: AdminEditRecipe.EDIT_RECIPE_NAME,
    ButtonTranslations.ADMIN_EDIT_RECIPE_DESCRIPTION: AdminEditRecipe.EDIT_RECIPE_DESCRIPTION,
    ButtonTranslations.ADMIN_EDIT_RECIPE_IMAGE: AdminEditRecipe.EDIT_RECIPE_IMAGE,
}

ratio_state_and_property_name_dict = {
    AdminEditRecipe.EDIT_RECIPE_NAME: 'name',
    AdminEditRecipe.EDIT_RECIPE_DESCRIPTION: 'description',
    AdminEditRecipe.EDIT_RECIPE_IMAGE: 'image_id',
}
    

@router.message(F.text.in_(list(ratio_buttons_and_message_dict.keys())) , AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def request_property(message: types.Message, state: FSMContext):
    msg = ratio_buttons_and_message_dict.get(message.text or '', '')
    new_state = ratio_buttons_and_state_dict.get(message.text or '')

    await state.set_state(new_state)
    await message.answer(
        text=msg,
        keyboard=CancelReplyKeyboard()
    )


@router.message(AdminEditRecipe.EDIT_RECIPE_NAME, F.text, AdminFilter())
@router.message(AdminEditRecipe.EDIT_RECIPE_DESCRIPTION, F.text, AdminFilter())
@router.message(AdminEditRecipe.EDIT_RECIPE_IMAGE, F.photo, AdminFilter())
async def update_property(message: types.Message, state: FSMContext):
    current_state: State = await state.get_state() # type: ignore
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    value = ''
    if message.photo:
        value = message.photo[-1].file_id
    elif message.text:
        value = message.text

    key = ratio_state_and_property_name_dict.get(current_state, '')
    update_values = {
        key: value
    }

    await RecipeService.update_recipe(
        recipe_id=recipe_id,
        **update_values
        )
        
    await message.answer(
        text=MessageTranslations.ADMIN_RECIPE_UPDATED,
        keyboard=EditRecipeReplyKeyboard()
    )

@router.message(AdminEditRecipe.EDIT_RECIPE_ADD_TAG, AdminFilter())
@router.message(F.text == ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_TAG, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def add_tag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    if message.text not in [*CATEGORY_BUTTONS, ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_TAG]:
        msg = MessageTranslations.ADMIN_RECIPE_UPDATED
        await RecipeService.add_tag_to_recipe(
            recipe_id=recipe_id,
            tag_name=message.text
        )
        
        await message.answer(
            reply_markup=EditRecipeReplyKeyboard(),
            text=msg,
        )
        return 
    
    offset = TagService.get_offset_tags(data.get('offset', 0)) 

    keyboard = await TagService.get_tags_not_in_recipe_keyboard(
        offset=offset,
        limit=10,
        recipe_id=recipe_id
    )

    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_ADD_TAG
    await state.set_state(AdminEditRecipe.EDIT_RECIPE_ADD_TAG)
    await message.answer(
        reply_markup=keyboard.as_markup(resize_keyboard=True),
        text=msg,
    )

@router.message(AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT, AdminFilter())
@router.message(F.text == ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_INGREDIENT, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def request_ingredient(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_ingredient = data.get('new_ingredient', {})
    recipe_id = data.get('recipe_id', 0)

    if message.text and message.text not in [*tag_list_manage_buttons, ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_INGREDIENT]:
        ingredient = await IngredientService.get_ingredient_by_name(message.text)
        if ingredient:
            new_ingredient['ingredient_id'] = ingredient.id
            await state.update_data(new_ingredient=new_ingredient)
            await state.set_state(AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT)
            
        return await request_ingredient_amount_type(message, state)
    
    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_ADD_INGREDIENT
    offset = IngredientService.get_offset_ingredients(data.get('offset',0))

    keyboard = await IngredientService.get_ingredients_not_in_recipe_keyboard(
        recipe_id=recipe_id,
        limit=10,
        offset=offset,
    )
    new_state = AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT
    if keyboard is None:
        msg = MessageTranslations.ADMIN_UPDATE_RECIPE_ADD_NO_INGREDIENTS_IN_DB
        await message.answer(
            text=msg,
        )
        return 

    await state.set_state(new_state)
    await message.answer(
        text=msg,
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )
    
async def request_ingredient_amount_type(message: types.Message, state: FSMContext):
    keyboard = IngredientService.get_ingredient_amount_types_keyboard()

    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_ADD_INGREDIENT_AMOUNT_TYPE
    await state.set_state(AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT_AMOUNT_TYPE)
    await message.answer(
        text=msg,
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )

@router.message(AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT_AMOUNT_TYPE, AdminFilter())
async def request_ingredient_amount(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_ingredient = data.get('new_ingredient', {})

    if message.text:
        amount_type: IngredientAmountTypeEnum | None = IngredientAmountTypeEnum.get_from_annotation(message.text)
        new_ingredient['amount_type'] = amount_type.name if amount_type else 'LITER'

    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_ADD_INGREDIENT_AMOUNT
    
    await state.update_data(new_ingredient=new_ingredient)
    await state.set_state(AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT_AMOUNT)
    await message.answer(
        text=msg,
        reply_markup=CancelReplyKeyboard(is_admin=is_admin)
    )


@router.message(AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT_AMOUNT, AdminFilter())
async def add_ingredient(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)
    new_ingredient = data.get('new_ingredient', {})

    keyboard = CancelReplyKeyboard(is_admin=is_admin)
    msg = MessageTranslations.INVALID_VALUE_IS_NOT_DIGIT
    new_state = AdminEditRecipe.EDIT_RECIPE_ADD_INGREDIENT_AMOUNT
    if message.text and message.text.isdigit():
        new_ingredient['amount'] = int(message.text)
        await RecipeService.add_ingredient_to_recipe(recipe_id, new_ingredient)

        new_ingredient = None
        msg = MessageTranslations.ADMIN_RECIPE_UPDATED
        keyboard = EditRecipeReplyKeyboard()
        new_state = AdminEditRecipe.EDIT_RECIPE
    
    await state.update_data(new_ingredient=new_ingredient)
    await state.set_state(new_state)
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )


@router.message(F.text == ButtonTranslations.ADMIN_EDIT_RECIPE_ADD_STEP, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def request_step_name(message: types.Message, state: FSMContext, is_admin: bool):
    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_ADD_STEP_DESCRIPTION
    keyboard = CancelReplyKeyboard(is_admin=is_admin)

    await state.set_state(AdminEditRecipe.EDIT_RECIPE_ADD_STEP_DESCRIPTION)
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )

@router.message(AdminEditRecipe.EDIT_RECIPE_ADD_STEP_DESCRIPTION, AdminFilter())
async def request_step_image(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_step = data.get('new_step', {})

    new_step['description'] = message.text

    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_ADD_STEP_IMAGE
    keyboard = CancelReplyKeyboard(is_admin=is_admin)

    await state.set_state(AdminEditRecipe.EDIT_RECIPE_ADD_STEP_IMAGE)
    await state.update_data(new_step=new_step)
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )

@router.message(F.photo, AdminEditRecipe.EDIT_RECIPE_ADD_STEP_IMAGE, AdminFilter())
async def add_step(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)
    new_step = data.get('new_step', {})

    if message.photo:
        new_step['image_id'] = message.photo[-1].file_id

    await RecipeService.add_step_to_recipe(
        recipe_id=recipe_id,
        new_step=new_step
    )

    msg = MessageTranslations.ADMIN_RECIPE_UPDATED
    keyboard = EditRecipeReplyKeyboard()
    await state.set_state(AdminEditRecipe.EDIT_RECIPE)
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )

@router.message(F.text == ButtonTranslations.ADMIN_EDIT_RECIPE_CHANGE_STEP_INDEXES, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def request_step_indexes(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)
    msg=MessageTranslations.ADMIN_UPDATE_RECIPE_STEPS_INDEX

    msg_steps = await RecipeService.get_recipe_steps_message(recipe_id)
    keyboard = CancelReplyKeyboard()
    if msg_steps is None:
        await message.answer(
            text=MessageTranslations.ADMIN_UPDATE_RECIPE_DELETE_NO_STEP
        )
        return 
    

    await state.set_state(AdminEditRecipe.EDIT_RECIPE_CHANGE_INDEXES)
    await message.answer(
        text=msg
    )
    await message.answer(
        text=msg_steps,
        reply_markup=keyboard,
    )

@router.message(F.text, AdminEditRecipe.EDIT_RECIPE_CHANGE_INDEXES, AdminFilter())
async def update_step_indexes(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    if message.text:
        # try:
        indexes = list(map(lambda x: int(x), message.text.split(' ')))

        await RecipeService.change_steps_indexes(recipe_id=recipe_id,indexes=indexes)

        keyboard = EditRecipeReplyKeyboard()
        msg = MessageTranslations.ADMIN_RECIPE_UPDATED
        new_state = AdminEditRecipe.EDIT_RECIPE
        # except Exception as e:
        #     keyboard = CancelReplyKeyboard()
        #     msg = MessageTranslations.INVALID_INDEXES_STRING_NOT_DIGIT
        #     new_state = AdminEditRecipe.EDIT_RECIPE_CHANGE_INDEXES

    await state.set_state(new_state)
    await message.answer(
        reply_markup=keyboard,
        text=msg
    )


@router.message(F.text == ButtonTranslations.ADMIN_EDIT_RECIPE_DELETE_TAG, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def request_delete_recipe_tag(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    keyboard = await RecipeService.get_recipe_tags_keyboard(recipe_id=recipe_id)
    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_DELETE_TAG

    await state.set_state(AdminEditRecipe.EDIT_RECIPE_DELETE_TAG)
    await message.answer(
        text=msg,
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )


@router.message(F.text, AdminEditRecipe.EDIT_RECIPE_DELETE_TAG, AdminFilter())
async def delete_recipe_tag(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    if message.text:
        await RecipeService.delete_recipe_tag_by_name(recipe_id=recipe_id, tag_name=message.text)

    keyboard = EditRecipeReplyKeyboard()
    msg = MessageTranslations.ADMIN_RECIPE_UPDATED

    await state.set_state(AdminEditRecipe.EDIT_RECIPE)
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )


@router.message(F.text == ButtonTranslations.ADMIN_EDIT_RECIPE_DELETE_INGREDIENT, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def request_delete_recipe_ingredient(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    keyboard = await RecipeService.get_recipe_ingredients_keyboard(recipe_id=recipe_id)
    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_DELETE_INGREDIENT

    await state.set_state(AdminEditRecipe.EDIT_RECIPE_DELETE_INGREDIENT)
    await message.answer(
        text=msg,
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )

@router.message(F.text, AdminEditRecipe.EDIT_RECIPE_DELETE_INGREDIENT, AdminFilter())
async def delete_recipe_ingredient(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    if message.text:
        await RecipeService.delete_recipe_ingredient_by_name(recipe_id=recipe_id, ingredient_name=message.text)

    keyboard = EditRecipeReplyKeyboard()
    msg = MessageTranslations.ADMIN_RECIPE_UPDATED

    await state.set_state(AdminEditRecipe.EDIT_RECIPE)
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )

@router.message(F.text == ButtonTranslations.ADMIN_EDIT_RECIPE_DELETE_STEP, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def request_delete_recipe_step(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    keyboard = await RecipeService.get_recipe_steps_keyboard(recipe_id=recipe_id)

    if keyboard is None:
        await message.answer(
            text=MessageTranslations.ADMIN_UPDATE_RECIPE_DELETE_NO_STEP,
        )
        return 
    msg = MessageTranslations.ADMIN_UPDATE_RECIPE_DELETE_STEP
    await state.set_state(AdminEditRecipe.EDIT_RECIPE_DELETE_STEP)
    await message.answer(
        text=msg,
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )

@router.message(AdminEditRecipe.EDIT_RECIPE_DELETE_STEP, AdminFilter())
async def delete_recipe_step(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    await RecipeService.delete_recipe_step_by_index(
        recipe_id=recipe_id,
        message=message.text or ''
        )
    msg = MessageTranslations.ADMIN_RECIPE_UPDATED

    await state.set_state(AdminEditRecipe.EDIT_RECIPE)
    await message.answer(
        text=msg,
        reply_markup=EditRecipeReplyKeyboard()
    )


@router.message(AdminEditRecipe.DELETE_RECIPE, AdminFilter())
@router.message(F.text == ButtonTranslations.ADMIN_DELETE_RECIPE, AdminEditRecipe.EDIT_RECIPE, AdminFilter())
async def delete_recipe(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    recipe_id = data.get('recipe_id', 0)

    if message.text == ButtonTranslations.YES:
        msg = MessageTranslations.ADMIN_DELETED_RECIPE
        new_state = None
        keyboard = MainMenuReplyKeyboard(is_admin=is_admin)

        await state.clear()
        await RecipeService.delete_recipe(recipe_id=recipe_id)
    elif message.text == ButtonTranslations.NO:
        msg = ButtonTranslations.NO
        new_state = AdminEditRecipe.EDIT_RECIPE
        keyboard = EditRecipeReplyKeyboard()
    else:
        msg = MessageTranslations.ADMIN_DELETE_RECIPE
        new_state = AdminEditRecipe.DELETE_RECIPE
        keyboard = ConfirmDeleteReplyKeyboard()

    await state.set_state(new_state)
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )
