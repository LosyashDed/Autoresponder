import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import load_config
from handlers.user_handlers import user_router
from middlewares.subscription import SubscriptionMiddleware

async def main():
    logging.basicConfig(level=logging.INFO)

    config = load_config('.env')
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    
    subscription_middleware = SubscriptionMiddleware(channel_id=config.channel_id, channel_url=config.channel_url)
    user_router.message.middleware(subscription_middleware)
    user_router.callback_query.middleware(subscription_middleware)

    dp["config"] = config
    
    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

