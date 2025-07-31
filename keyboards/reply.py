from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from services import CONSULTATION_TYPES

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in CONSULTATION_TYPES:
        builder.add(KeyboardButton(text=item))
    
    builder.adjust(2)
    
    return builder.as_markup(resize_keyboard=True)
