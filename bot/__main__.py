import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config_reader import config
from handlers import cmd_handlers
from handlers.FSM import search_city
from handlers import inline_handlers
from middlewares.database import DbSessionMiddleware


async def on_startup(dp, bot):
    await bot.set_webhook(config.webhook_url)
    print(f'Telegram servers now send updates to {config.webhook_url}. Bot is online')


async def on_shutdown(dp, bot):
    await bot.delete_webhook(config.webhook_url)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    engine = create_async_engine(url=config.db_url.__str__(), echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    redis_storage = RedisStorage.from_url(config.redis_url.__str__())

    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher(storage=redis_storage)

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(cmd_handlers.router)
    dp.include_router(search_city.router)
    dp.include_router(inline_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)

    if config.webhook:
        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot
        )
        webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)
    else:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
