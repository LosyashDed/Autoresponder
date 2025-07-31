from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_channel_keyboard(channel_url: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Перейти к каналу", url=channel_url),
        ],
        [
            InlineKeyboardButton(text="Я подписался(ась)", callback_data="check_subscription")
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_contact_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="По телефону", callback_data="contact_phone"),
            InlineKeyboardButton(text="В сообщениях", callback_data="contact_messages")
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
