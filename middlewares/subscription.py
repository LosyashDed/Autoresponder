from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.flags import get_flag
from keyboards.inline import get_channel_keyboard

class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, channel_id: str, channel_url: str):
        self.channel_id = channel_id
        self.channel_url = channel_url

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if get_flag(data, "subscription") is None:
            return await handler(event, data)

        user_id = event.from_user.id
        bot = data.get('bot')

        member = await bot.get_chat_member(chat_id=self.channel_id, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return await handler(event, data)

        text = "Здравствуйте! Чтобы получить доступ к функциям бота и забрать свой подарок, пожалуйста, подпишитесь на наш канал."
        
        await event.answer(text, reply_markup=get_channel_keyboard(self.channel_url))
