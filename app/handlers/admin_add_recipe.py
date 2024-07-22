from curses.ascii import isdigit
from mailbox import Message
from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.filters.admin import AdminFilter
from app.keyboards.admin import AdminAddMoreStepReplyKeyboard, AdminPanelReplyKeyboard
from app.keyboards.base import ReplyKeyboardBase
from app.keyboards.main_menu import MainMenuReplyKeyboard
from app.keyboards.recipe import CancelReplyKeyboard
from app.models.enum import IngredientAmountTypeEnum
from app.service.admin import AdminService
from app.service.admin_add_recipe import AdminAddRecipeService
from app.service.ingredient import IngredientService
from app.service.tag import TagService, tag_list_manage_buttons
from app.translations import ButtonTranslations, MessageTranslations


router = Router(name='admin_add_recipe')

class AdminRecipe(StatesGroup):
    ADD_RECIPE_NAME = State()
    ADD_RECIPE_DESCRIPTION = State()
    ADD_RECIPE_IMAGE = State()
    ADD_RECIPE_TAGS = State()
    ADD_RECIPE_INGREDIENT = State()
    ADD_RECIPE_INGREDIENT_AMOUNT_TYPE = State()
    ADD_RECIPE_INGREDIENT_AMOUNT= State()

    ADD_RECIPE_STEP = State()
    ADD_RECIPE_STEP_DESCRIPTION = State()
    ADD_RECIPE_STEP_IMAGE = State()
    ADD_RECIPE_DONE_OR_MORE_STEP = State()


@router.message(F.text == ButtonTranslations.ADMIN_ADD_RECIPE, AdminFilter())
async def add_recipe(message: types.Message, state: FSMContext, is_admin:bool):
    await state.set_data({
        'new_recipe': {}
    })
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_RECIPE
    )
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_RECIPE_NAME,
        reply_markup=CancelReplyKeyboard(is_admin=is_admin)
    )
    await state.set_state(AdminRecipe.ADD_RECIPE_NAME)


@router.message(AdminRecipe.ADD_RECIPE_NAME, F.text, AdminFilter())
@router.message(AdminRecipe.ADD_RECIPE_DESCRIPTION, F.text, AdminFilter())
@router.message(AdminRecipe.ADD_RECIPE_IMAGE, F.photo, AdminFilter())
async def add_recipe_string_value(message: types.Message, state: FSMContext, is_admin: bool):
    new_recipe = (await state.get_data()).get('new_recipe', {})
    state_type = await state.get_state()

    msg = None
    match state_type:
        case AdminRecipe.ADD_RECIPE_NAME:
            new_state = AdminRecipe.ADD_RECIPE_DESCRIPTION
            new_recipe['name'] = message.text
            msg = MessageTranslations.ADMIN_ADD_RECIPE_DESCRIPTION

        case AdminRecipe.ADD_RECIPE_DESCRIPTION:
            new_state = AdminRecipe.ADD_RECIPE_IMAGE
            new_recipe['description'] = message.text
            msg = MessageTranslations.ADMIN_ADD_RECIPE_IMAGE

        case AdminRecipe.ADD_RECIPE_IMAGE:
            if (message.photo):
                new_state = AdminRecipe.ADD_RECIPE_TAGS
                new_recipe['image_id'] = message.photo[-1].file_id      

    
    if msg:
        await message.answer(
            text=msg,
            reply_markup=CancelReplyKeyboard(is_admin=is_admin)
        )
    await state.set_state(new_state)
    await state.update_data(new_recipe=new_recipe)

    if new_state == AdminRecipe.ADD_RECIPE_TAGS:
        return await add_recipe_tags(message, state, is_admin)


@router.message(AdminRecipe.ADD_RECIPE_TAGS, F.text, AdminFilter())
async def add_recipe_tags(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_recipe: dict = data.get('new_recipe', {})
    tags: list = new_recipe.get('tags', [])

    if message.text == ButtonTranslations.DONE:
        await state.set_state(AdminRecipe.ADD_RECIPE_INGREDIENT)
        await state.update_data(add_new_ingredient=True)
        return await add_recipe_ingredient(message, state, is_admin)

    if message.text and message.text not in tag_list_manage_buttons:
        tag = await TagService.get_tag_by_name(message.text)
        tags.append(tag.id if tag else 0)

    offset = TagService.get_offset_tags(message.text, data.get('offset_tags', 0))
    limit = 10
    
    keyboard = await AdminAddRecipeService.get_add_tags_keyboard(
        offset=offset,
        limit=limit
    )
    msg = MessageTranslations.ADMIN_ADD_RECIPE_TAGS

    await message.answer(
        text=msg,
        reply_markup=keyboard.as_markup(resize_keyboard=True)
    )
    new_recipe['tags'] = tags
    await state.update_data(new_recipe=new_recipe)


@router.message(AdminRecipe.ADD_RECIPE_INGREDIENT, F.text, AdminFilter())
async def add_recipe_ingredient(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    add_new_ingredient: bool = data.get('add_new_ingredient', False)
    add_new_ingredient_more: bool = data.get('add_new_ingredient_more', False)
    new_recipe: dict = data.get('new_recipe', {})
    new_ingredient: dict = data.get('new_ingredient', {})

    if message.text == ButtonTranslations.DONE and not add_new_ingredient:
        await message.answer(
            text=MessageTranslations.ADMIN_ADD_RECIPE_STEP,
        )
        await message.answer(
            text=MessageTranslations.ADMIN_ADD_RECIPE_STEP_DESCRIPTION,
            reply_markup=CancelReplyKeyboard(is_admin=is_admin)
        )

        await state.set_state(AdminRecipe.ADD_RECIPE_STEP_DESCRIPTION)
        return 

    if message.text and message.text not in tag_list_manage_buttons:
        ingredient = await IngredientService.get_ingredient_by_name(message.text)
        new_ingredient['ingredient_id'] = ingredient.id if ingredient else 0

    if add_new_ingredient:
        offset = TagService.get_offset_tags(message.text, data.get('offset_tags', 0))
        limit = 10
        
        keyboard = await AdminAddRecipeService.get_add_ingredients_keyboard(
            offset=offset,
            limit=limit
        )
        msg =  MessageTranslations.ADMIN_ADD_RECIPE_INGREDIENT_MORE if add_new_ingredient_more else MessageTranslations.ADMIN_ADD_RECIPE_INGREDIENT
        new_state = AdminRecipe.ADD_RECIPE_INGREDIENT

    else:
        msg = MessageTranslations.ADMIN_ADD_RECIPE_INGREDIENT_AMOUNT_TYPE
        keyboard = IngredientService.get_ingredient_amount_types_keyboard()
        new_state = AdminRecipe.ADD_RECIPE_INGREDIENT_AMOUNT_TYPE
    
    await state.set_state(new_state)
    await state.update_data(new_recipe=new_recipe, new_ingredient=new_ingredient, add_new_ingredient=None, add_new_ingredient_more=None)

    await message.answer(
            text=msg,
            reply_markup=keyboard.as_markup(resize_keyboard=True)
        )


@router.message(AdminRecipe.ADD_RECIPE_INGREDIENT_AMOUNT_TYPE, F.text, AdminFilter())
async def add_recipe_ingredient_amount_type(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_recipe: dict = data.get('new_recipe', {})
    new_ingredient: dict = data.get('new_ingredient', {})

    if message.text:
        amount_type: IngredientAmountTypeEnum | None = IngredientAmountTypeEnum.get_from_annotation(message.text)
        new_ingredient['amount_type'] = amount_type.value if amount_type else 1

    msg = MessageTranslations.ADMIN_ADD_RECIPE_INGREDIENT_AMOUNT

    
    await state.update_data(new_recipe=new_recipe, new_ingredient=new_ingredient)
    await state.set_state(AdminRecipe.ADD_RECIPE_INGREDIENT_AMOUNT)
    await message.answer(
        text=msg,
        reply_markup=CancelReplyKeyboard(is_admin=is_admin)
    )
    

@router.message(AdminRecipe.ADD_RECIPE_INGREDIENT_AMOUNT, F.text, AdminFilter())
async def add_recipe_ingredient_amount(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_recipe: dict = data.get('new_recipe', {})
    ingredients: list = new_recipe.get('ingredients', [])
    new_ingredient: dict = data.get('new_ingredient', {})

    if message.text and message.text.isdigit():
        new_ingredient['amount'] = int(message.text)
        ingredients.append(new_ingredient)
        msg = MessageTranslations.ADMIN_ADD_RECIPE_INGREDIENT_ADDED
        keyboard=None
    else:
        msg = MessageTranslations.INVALID_VALUE_IS_NOT_DIGIT
        keyboard = CancelReplyKeyboard(is_admin=is_admin)
    
    await message.answer(
        text=msg,
        reply_markup=keyboard
    )
    
    if new_ingredient['amount']:
        new_recipe['ingredients'] = ingredients
        await state.update_data(new_recipe=new_recipe, new_ingredient={}, add_new_ingredient=True, add_new_ingredient_more=True)
        await state.set_state(AdminRecipe.ADD_RECIPE_INGREDIENT)
        return await add_recipe_ingredient(message, state, is_admin)
        

@router.message(AdminRecipe.ADD_RECIPE_STEP_DESCRIPTION, F.text, AdminFilter())
async def add_recipe_step_description(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_step: dict = data.get('new_step', {})

    if message.text:
        new_step['description'] = message.text

    await state.set_state(AdminRecipe.ADD_RECIPE_STEP_IMAGE)
    await state.update_data(new_step=new_step)
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_RECIPE_STEP_IMAGE,
        reply_markup=CancelReplyKeyboard(is_admin=is_admin)
    )


@router.message(AdminRecipe.ADD_RECIPE_STEP_IMAGE, F.photo, AdminFilter())
async def add_recipe_step_image(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_step: dict = data.get('new_step', {})
    new_recipe: dict = data.get('new_recipe', {})
    steps: list = new_recipe.get('steps', [])

    if message.photo:
        new_step['image_id'] = message.photo[-1].file_id 

    steps.append(new_step)

    new_recipe['steps'] = steps
    await state.set_state(AdminRecipe.ADD_RECIPE_DONE_OR_MORE_STEP)
    await state.update_data(new_recipe=new_recipe, new_step={})
    await message.answer(
        text=MessageTranslations.ADMIN_ADD_RECIPE_STEP_MORE,
        reply_markup=AdminAddMoreStepReplyKeyboard(is_admin=is_admin)
    )


@router.message(AdminRecipe.ADD_RECIPE_DONE_OR_MORE_STEP, F.text, AdminFilter())
async def choose_add_step_or_done(message: types.Message, state: FSMContext, is_admin: bool):
    data = await state.get_data()
    new_recipe: dict = data.get('new_recipe', {})

    if message.text == ButtonTranslations.ADMIN_ADD_STEP_MORE:
        await message.answer(
            text=MessageTranslations.ADMIN_ADD_RECIPE_STEP_DESCRIPTION,
            reply_markup=CancelReplyKeyboard(is_admin=is_admin)
        )

        await state.set_state(AdminRecipe.ADD_RECIPE_STEP_DESCRIPTION)
        return 

    if message.text == ButtonTranslations.DONE:

        await AdminAddRecipeService.add_recipe_from_dict(new_recipe)
        await state.clear()
        return await message.answer(
            text=MessageTranslations.ADMIN_ADD_RECIPE_SAVED,
            reply_markup=AdminPanelReplyKeyboard(is_admin=is_admin)
        )
    
    await message.answer(
        text=MessageTranslations.CHOOSE_BUTTON_OPTION
    )