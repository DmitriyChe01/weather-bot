from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.callback_data import CancelCallbackData, CityCallbackData, WeatherDayCallbackData
from utils import generate_ten_days_of_the_week

from gismeteo.queries import City


def generate_city_inline_kb(cities: list[City]) -> InlineKeyboardMarkup:
    """Возвращает инлайн клавиатуру со списком городов"""
    inline_markup = InlineKeyboardBuilder()
    for c in cities:
        inline_markup.row(InlineKeyboardButton(text=c.city_name,
                                               callback_data=CityCallbackData(city_id=c.city_id,
                                                                              city_name=c.city_name).pack()))
    return inline_markup.as_markup()


def generate_weather_date_kb(city_id: int) -> InlineKeyboardMarkup:
    """Возвращает инлайн клавиатуру со списком дат"""
    days = generate_ten_days_of_the_week()
    inline_markup = InlineKeyboardBuilder()
    for i, day in enumerate(days):
        callback_data = WeatherDayCallbackData(city_id=city_id, day_number=i).pack()
        inline_markup.row(InlineKeyboardButton(text=day, callback_data=callback_data))
    return inline_markup.as_markup()


def cancel() -> InlineKeyboardMarkup:
    """Возвращает кнопку отмены"""
    inline_markup = InlineKeyboardBuilder()
    inline_markup.row(InlineKeyboardButton(text='Отмена', callback_data=CancelCallbackData().pack()))
    return inline_markup.as_markup()
