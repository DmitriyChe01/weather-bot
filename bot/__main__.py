import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from middlewares.database import DbSessionMiddleware
from config_reader import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers import cmd_handlers
from handlers.FSM import search_city
from handlers import inline_handlers


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    engine = create_async_engine(url=config.db_url.__str__(), echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(cmd_handlers.router)
    dp.include_router(search_city.router)
    dp.include_router(inline_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
