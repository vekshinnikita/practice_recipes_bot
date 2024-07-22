
from abc import ABC, abstractmethod
from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from app.types.keyboard import AnyKeyboard


class KeyboardBase(ABC):
    __class_base__: type[InlineKeyboardMarkup] | type[ReplyKeyboardMarkup]
    
    def __new__(cls, *args, **kwargs):
        attrs = {}
        for key, value in cls.__dict__.items():
            if not key.startswith('_') and \
                key not in ('keyboard', 'inline_keyboard') and \
                not callable(open):
                attrs[key] = value 

        keyboard = cls._get_keyboard(kwargs.get('is_admin', False))
        keyboard_key = 'inline_keyboard' if cls.__class_base__ == InlineKeyboardMarkup else 'keyboard'
        attrs[keyboard_key] = keyboard


        if cls.__class_base__ is None:
            raise RuntimeError("__class_base__ does not define")
        
        return cls.__class_base__(**attrs)
    
    @classmethod
    def _get_keyboard(cls, is_admin: bool):
        if is_admin:
            return cls.get_admin_keyboard()
        return cls._get_keyboard_attr()
    
    @classmethod
    @abstractmethod
    def _get_keyboard_attr(cls):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def get_admin_keyboard(cls):
        raise NotImplementedError


class ReplyKeyboardBase(KeyboardBase):
    __class_base__: type[ReplyKeyboardMarkup] = ReplyKeyboardMarkup
 
    keyboard: List[List[KeyboardButton]] = []
    is_persistent: bool | None = None
    resize_keyboard: bool | None = None
    one_time_keyboard: bool | None = None
    input_field_placeholder: str | None = None
    selective: bool | None = None

    def __new__(cls, *args, **kwargs) -> ReplyKeyboardMarkup:
        return super().__new__(cls, *args, **kwargs) #type: ignore

    @classmethod
    def _get_keyboard_attr(cls):
        return cls.keyboard
    
    @classmethod
    def get_admin_keyboard(cls) -> List[List[KeyboardButton]]:
        return cls.keyboard
    

class InlineKeyboardBase(KeyboardBase):
    __class_base__: type[InlineKeyboardMarkup] = InlineKeyboardMarkup
 
    inline_keyboard: List[List[InlineKeyboardButton]] = []

    def __new__(cls, *args, **kwargs) -> InlineKeyboardMarkup:
        return super().__new__(cls, *args, **kwargs) #type: ignore

    @classmethod
    def _get_keyboard_attr(cls):
        return cls.inline_keyboard
    
    @classmethod
    def get_admin_keyboard(cls) -> List[List[InlineKeyboardButton]]:
        return cls.inline_keyboard
    

class CombineInlineKeyboards(InlineKeyboardBase):

    def __new__(cls, *args: InlineKeyboardMarkup | None):
        cls.inline_keyboard = []
        for keyboard in args:
            if keyboard is not None:
                cls.inline_keyboard.extend(keyboard.inline_keyboard)
    
        return super().__new__(cls)


class CombineReplyKeyboards(ReplyKeyboardMarkup):

    def __new__(cls, *args: ReplyKeyboardMarkup | None):
        cls.keyboard = []
        for keyboard in args:
            if keyboard is not None:
                cls.keyboard.extend(keyboard.keyboard)
    
        return super().__new__(cls)