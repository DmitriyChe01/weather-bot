import logging

from sqlalchemy import ChunkedIteratorResult
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from aiogram import types

from db import TelegramUser, City, city_telegram_user_table
from typing import Dict, Any
from bot.gismeteo.queries import City as CityCallbackData

from filters.callback_data import CityCallbackData
from db.models import city_telegram_user_table as city_user


async def get_or_create_user(session: AsyncSession, data: Dict[str, Any]):
    user_instance = await session.execute(
        select(TelegramUser).where(TelegramUser.user_id == data["event_from_user"].id))
    user = user_instance.scalar_one_or_none()
    context_user = data["event_from_user"]
    if user:
        return user
    else:
        new_user = TelegramUser(user_id=context_user.id,
                                is_bot=context_user.is_bot,
                                first_name=context_user.first_name,
                                last_name=context_user.last_name,
                                username=context_user.username,
                                language_code=context_user.language_code,
                                is_premium=context_user.is_premium,

                                )
        await session.merge(new_user)
        await session.commit()
        return new_user


async def create_city(session: AsyncSession, callback_data: CityCallbackData):
    instance_city = await session.execute(select(City)
                                          .where(City.city_id == callback_data.city_id))
    city: City or None = instance_city.scalar_one_or_none()
    if city is None:
        session.add(City(city_id=callback_data.city_id, city_name=callback_data.city_name))
        await session.commit()


async def create_user_history(session: AsyncSession, callback_data: CityCallbackData, query: types.CallbackQuery):
    stmt = insert(city_telegram_user_table).values(city_id=callback_data.city_id,
                                                   telegram_user_id=query.from_user.id)
    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        logging.info("Уже существует")


async def get_last_user_history(session: AsyncSession, message: types.Message) -> list[CityCallbackData]:
    cursor = await session.execute(select(city_user.c.city_id, City.city_name).distinct(city_user.c.city_id)
                                   .join(City, city_user.c.city_id == City.city_id)
                                   .where(city_user.c.telegram_user_id == message.from_user.id)
                                   .order_by(city_user.c.city_id, city_user.c.datetime.desc())
                                   .limit(8))
    return [CityCallbackData(**i) for i in cursor.mappings().all()]
