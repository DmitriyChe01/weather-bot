import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import load_config

from bot.handlers import cmd_handlers
from bot.handlers.FSM import search_city
from bot.handlers import inline_handlers


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config = load_config()
    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(cmd_handlers.router)
    dp.include_router(search_city.router)
    dp.include_router(inline_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
