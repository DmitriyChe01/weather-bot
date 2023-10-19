from dataclasses import dataclass
from aiopygismeteo import Gismeteo
from pygismeteo_base import models
from .parsers import parse_weather_step24_model, parse_weather_model

gismeteo = Gismeteo()


@dataclass
class City:
    city_name: str
    city_id: int


async def search_city(city: str) -> list[City] | None:
    """Ищет по названию город и возвращает объект с названием и id города"""
    response = await gismeteo.search.by_query(city)
    if response:
        return list(map(lambda item: City(item.name, item.id), response))


async def get_weather_current(city_id: int) -> str:
    """Возвращает погоду на сегодня"""
    weather: models.step24.Model = await gismeteo.step24.by_id(city_id, days=3)
    return ''.join(parse_weather_step24_model(weather[0]))


async def get_weather_current_3hours(city_id: int) -> str:
    """Возвращает погоду на сегодня с шагом 3 часа"""
    weather: models.step3.Model = await gismeteo.step3.by_id(city_id, days=1)
    messages: list[str] = []
    [messages.append(parse_weather_model(item)) for item in weather]
    return ''.join(messages)


async def get_weather_3days_6hours(city_id: int) -> str:
    """Возвращает погоду на 3 дня с шагом 6 часов"""
    weather: models.step6.Model = await gismeteo.step6.by_id(city_id, days=3)
    messages: list[str] = []
    [messages.append(parse_weather_model(item)) for item in weather]
    return ''.join(messages)


async def get_weather_3days_24hours(city_id: int) -> str:
    """Возвращает погоду на 3 дня с шагом 24 часа"""
    weather: models.step24.Model = await gismeteo.step24.by_id(city_id, days=3)
    messages: list[str] = []
    [messages.append(parse_weather_step24_model(item)) for item in weather]
    return ''.join(messages)


async def get_weather_10days_24hours(city_id: int) -> str:
    """Возвращает погоду на 10 дней с шагом 24 часа"""
    weather: models.step24.Model = await gismeteo.step24.by_id(city_id, days=10)
    messages: list[str] = []
    [messages.append(parse_weather_step24_model(item)) for item in weather]
    return ''.join(messages)


async def get_weather_day_of_the_week(city_id: int, day_number: int) -> str:
    """Возвращает погоду на 1 день из 10 дней"""
    weather: models.step3.Model = await gismeteo.step3.by_id(city_id, days=10)
    messages: list[str] = []
    [messages.append(parse_weather_model(item)) for item in weather[day_number * 8:day_number * 8 + 8]]
    return ''.join(messages)
