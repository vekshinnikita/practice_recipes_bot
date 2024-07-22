from enum import Enum
from typing import Annotated




class EnumBase(Enum):

    def get_short_annotation(self) -> str:
        return self.__class__.__annotations__[self.name].__metadata__[0]
    
    def get_full_annotation(self) -> str:
        return self.__class__.__annotations__[self.name].__metadata__[1]
    
    @classmethod
    def get_from_annotation(cls, str: str):
        for key, annotation_list in cls.__annotations__.items():
            if str in annotation_list.__metadata__:
                return getattr(cls, key)
        
        return None


class IngredientAmountTypeEnum(EnumBase, Enum):
    LITER: Annotated[
        int, 
        "л.", 
        "Литры"
    ] = 1
    MILLILITER: Annotated[
        int, 
        "мл.",
        "Миллилитры"
    ] = 2

    MILLIGRAM: Annotated[
        int, 
        "мг.",
        "Миллиграммы"
    ] = 3
    GRAM: Annotated[
        int, 
        "г.",
        "Граммы"
    ] = 4
    KILOGRAM: Annotated[
        int, 
        "кг.",
        "Килограммы"
    ] = 5

    PIECE: Annotated[
        int, 
        "шт.",
        "Штуки"
    ] = 6
    PINCH: Annotated[
        int, 
        "шп.",
        "Щепотки"
    ] = 7

    SPOON: Annotated[
        int, 
        "лож.",
        "Ложки"
    ] = 8
    SMALL_SPOON: Annotated[
        int, 
        "мл. лож.",
        "Маленькие ложки"
    ] = 9

    TO_TASTE: Annotated[
        int, 
        "по вкусу",
        "по вкусу"
    ] = 10


class ImageTypeEnum(Enum):
    URL=1
    TG_ID=2

    