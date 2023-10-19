from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.query import create_city, create_user_history
from bot.keyboards.inline_buttons.keys import cancel, generate_city_inline_kb
from bot.states.weather_search import WeatherSearchStates
from bot.filters.callback_data import CancelCallbackData, CityCallbackData

from bot.gismeteo.queries import search_city
from bot.resources.res import COMMANDS_FOR_GET_WEATHER
from bot.gismeteo.queries import City

from bot.db.models import TelegramUser

router = Router()


@router.message(F.text == '>Узнать погоду')
async def weather_keyboard_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите название города:', reply_markup=cancel())
    await state.set_state(WeatherSearchStates.input_city_name)


@router.message(WeatherSearchStates.input_city_name, F.text)
async def input_city_name(message: types.Message, state: FSMContext):
    cities: list[City] = await search_city(message.text)
    if cities:
        await message.answer('Выберите город:', reply_markup=generate_city_inline_kb(cities))
        await state.set_state(WeatherSearchStates.choice_city_name)
    else:
        await message.answer('Ничего не найдено попробуйте ещё раз:', reply_markup=cancel())


@router.callback_query(WeatherSearchStates.choice_city_name, CityCallbackData.filter())
async def get_weather_in_city(query: types.CallbackQuery, callback_data: CityCallbackData, state: FSMContext,
                              session: AsyncSession, user: TelegramUser):
    await create_city(session, callback_data)
    await create_user_history(session, callback_data, query)

    weather_data = COMMANDS_FOR_GET_WEATHER.format(city_id=callback_data.city_id, city_name=callback_data.city_name)
    await state.update_data(city_name=callback_data.city_name)
    await query.message.answer(weather_data)
    await state.clear()


@router.callback_query(CancelCallbackData.filter())
async def cancel_inline_handler(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Отмена')
    await state.clear()
