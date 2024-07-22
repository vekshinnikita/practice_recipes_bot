from typing import Dict, List
from app.models.enum import IngredientAmountTypeEnum
from app.models.recipe import Recipe, RecipeIngredient, RecipeStep
from app.repository.ingredient import IngredientRepo
from app.repository.recipe import RecipeRepo
from app.repository.tag import TagRepo
from app.service.ingredient import IngredientService
from app.service.tag import TagService
from app.translations import ButtonTranslations


class AdminAddRecipeService:

    @classmethod
    async def get_add_tags_keyboard(cls, offset:int = 0, limit: int=10):
        keyboard = await TagService.get_tags_keyboard(
            offset=offset,
            limit=limit
        )
        
        keyboard.button(text=ButtonTranslations.DONE)
        keyboard.adjust(1)
        return keyboard
    
    @classmethod
    async def get_add_ingredients_keyboard(cls, offset:int = 0, limit: int=10):
        keyboard = await IngredientService.get_ingredients_keyboard(
            offset=offset,
            limit=limit
        )
        
        keyboard.button(text=ButtonTranslations.DONE)
        keyboard.adjust(2)
        return keyboard

    @classmethod
    async def add_recipe_from_dict(cls, new_recipe: dict):
        ingredients_data: list[dict] = new_recipe.get('ingredients', [])
        tag_ids: list[int] = new_recipe.get('tags', [])
        recipe_steps: List[Dict] = new_recipe.get('steps', [])
        
        recipe_ingredient_list = [
            RecipeIngredient(
                ingredient_id=ingredient_dict.get('ingredient_id'),
                amount=ingredient_dict.get('amount'),
                amount_type=IngredientAmountTypeEnum(ingredient_dict.get('amount_type', 1)),
            )
            for ingredient_dict in ingredients_data
        ]

        tags = await TagRepo.get_tags_by_ids(tag_ids)

        recipe_step_list = [
            RecipeStep(
                image_id=step.get('image_id', ''),
                sequence_number=index+1,
                description=step.get('description', '')
            )
            for index, step in enumerate(recipe_steps)
        ]

        recipe = Recipe(
            name=new_recipe.get('name', ''),
            nocase_name=new_recipe.get('name', '').lower(),
            description=new_recipe.get('description', ''),
            image_id=new_recipe.get('image_id', ''),
        )
        recipe.tags.extend(tags)
        recipe.steps.extend(recipe_step_list)
        recipe.ingredients.extend(recipe_ingredient_list)

        await RecipeRepo.add_recipe_from_model(recipe)