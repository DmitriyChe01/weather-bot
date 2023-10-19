from aiogram import Router
from aiogram import types

from bot.filters.callback_data import WeatherDayCallbackData
from bot.gismeteo.queries import get_weather_day_of_the_week

router = Router()


@router.callback_query(WeatherDayCallbackData.filter())
async def day_weather_inline_handler(query: types.CallbackQuery, callback_data: WeatherDayCallbackData):
    message = await get_weather_day_of_the_week(callback_data.city_id, callback_data.day_number)
    await query.message.edit_text(message)
