from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession

from filters.cmd_filters import CMDWeatherFilter, CMDWeatherDaysFilter
from keyboards.keyboard_buttons.screens import main_keyboard
from keyboards.inline_buttons.keys import generate_weather_date_kb, generate_city_inline_kb
from db.query import get_last_user_history
from states.weather_search import WeatherSearchStates

from gismeteo import queries

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    markup = main_keyboard()
    await message.answer('Привет. Это бот чтобы узнать погоду', reply_markup=markup)


@router.message(CMDWeatherFilter())
async def weather_cmd(message: Message):
    _, city_id, s = message.text[1:].split('@')[0].split('_')
    match s:
        case '1x1':
            text = await queries.get_weather_current(int(city_id))
            await message.answer(text)
        case '3x1':
            text = await queries.get_weather_current_3hours(int(city_id))
            await message.answer(text)
        case '6x3':
            text = await queries.get_weather_3days_6hours(int(city_id))
            await message.answer(text)
        case '24x3':
            text = await queries.get_weather_3days_24hours(int(city_id))
            await message.answer(text)
        case '24x10':
            text = await queries.get_weather_10days_24hours(int(city_id))
            await message.answer(text)


@router.message(CMDWeatherDaysFilter())
async def weather_days(message: Message):
    """Отправляет сообщение с инлайн кнопками для выбора  прогноза погоды"""
    _, city_id = message.text[1:].split('@')[0].split('_')
    await message.answer('Выберите день:', reply_markup=generate_weather_date_kb(city_id))


@router.message(F.text == '>Последние города')
async def history_cmd(message: Message, session: AsyncSession, state: FSMContext):
    city_callback_data = await get_last_user_history(session, message)
    inline_kb = generate_city_inline_kb(city_callback_data)
    await state.set_state(WeatherSearchStates.choice_city_name)
    if city_callback_data:
        await message.answer('Выберите город', reply_markup=inline_kb)
    else:
        await message.answer('Нет городов в истории')
