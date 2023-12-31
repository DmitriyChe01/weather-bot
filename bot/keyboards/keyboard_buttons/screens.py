from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


def main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='>Узнать погоду'),

    )
    builder.row(
        KeyboardButton(text='>Последние города')
    )

    return builder.as_markup(resize_keyboard=True)


def weather_step_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=''),
        KeyboardButton(text=''),
    )
