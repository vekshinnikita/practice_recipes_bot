from typing import List
from .enum import ImageTypeEnum, IngredientAmountTypeEnum
from .base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import BigInteger, Enum, ForeignKey, Integer


class Admin(Base):
    __tablename__ = 'admin'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    

class RecipeTag(Base):
    __tablename__ = 'recipe_tag'
    tag_id: Mapped[int] = mapped_column(ForeignKey('tag.id'), primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipe.id'), primary_key=True)
    

class Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    nocase_name: Mapped[str]
    description: Mapped[str]
    image_id: Mapped[str] = mapped_column(default='AgACAgIAAxkBAAIBZGaSt1IhzQ_4VFv6XJ47sk-cqSOVAAJ53zEbrtKRSKbJksRnkqr3AQADAgADeQADNQQ')

    steps: Mapped[List['RecipeStep']] = relationship("RecipeStep", back_populates='recipe', uselist=True, order_by='RecipeStep.sequence_number',  cascade='all, delete')
    ingredients: Mapped[List['RecipeIngredient']] = relationship("RecipeIngredient", back_populates='recipe', uselist=True,  cascade='all, delete')
    tags: Mapped[List['Tag']] = relationship("Tag", back_populates='recipes', uselist=True, secondary='recipe_tag',  cascade='all, delete')


class RecipeStep(Base):
    __tablename__ = 'recipe_step'

    id: Mapped[int] = mapped_column(primary_key=True)
    sequence_number: Mapped[int]
    description: Mapped[str]
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))
    image_id: Mapped[str] = mapped_column(default='AgACAgIAAxkBAAIBZGaSt1IhzQ_4VFv6XJ47sk-cqSOVAAJ53zEbrtKRSKbJksRnkqr3AQADAgADeQADNQQ')

    recipe: Mapped['Recipe'] = relationship("Recipe", back_populates='steps')


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredient'

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredient.id"), nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))
    amount: Mapped[int] = mapped_column(Integer, nullable=True)
    amount_type = mapped_column(Enum(IngredientAmountTypeEnum))

    recipe: Mapped['Recipe'] = relationship("Recipe", back_populates='ingredients')
    ingredient: Mapped['Ingredient'] = relationship("Ingredient")


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    recipes: Mapped[List['Recipe']] = relationship("Recipe", back_populates='tags', uselist=True, secondary='recipe_tag')
