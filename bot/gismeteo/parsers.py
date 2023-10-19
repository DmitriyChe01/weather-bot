from pygismeteo_base import models
from .res import SCALE_8, GM, STORM, PRECIPITATION, PHENOMENON


def parse_weather_model(city_model: models.current.Model or models.step6.Model) -> str:
    return (
        f'\t<b><u>------{city_model.date.local}------</u></b>\n'
        f'<b>{city_model.description.full}</b>\n'
        f'🌡️<b>Температура:</b> <u>{city_model.temperature.air.c}°С</u>\n'
        f'🧘<b>Ощущается:</b> <u>{city_model.temperature.comfort.c}°С</u>\n'
        f'♒<b>Влажность:</b> <u>{city_model.humidity.percent}%</u>\n'
        f'💨<b>Ветер:</b> <u>{SCALE_8.get(city_model.wind.direction.scale_8, "нет данных")}</u> '
        f'<u>{city_model.wind.speed.m_s} м/с</u>\n'
        
        f'☔<b>Осадки:</b> {STORM.get(city_model.storm)}'
        f'{PRECIPITATION["INTENSITY"].get(city_model.precipitation.intensity)} '
        f'{PRECIPITATION["TYPE"].get(city_model.precipitation.type)} {city_model.precipitation.amount} мм\n'
        
        f'🌪️<b>Погодное явление:</b> {PHENOMENON.get(city_model.phenomenon)}\n'
        f'🧲<b>Геомагнитное поле:</b> <u>{GM.get(city_model.gm, "нет данных")}</u>\n'
    )


def parse_weather_step24_model(city_model: models.step24.ModelItem) -> str:
    return (
        f'\t------{city_model.date.local}------\n'
        f'<b>{city_model.description.full}</b>\n'
        f'🌡️<b>Температура:</b> <u>{city_model.temperature.air.min.c}°С</u>|<u>{city_model.temperature.air.max.c}</u>°С\n'
        f'🧘<b>Ощущается:</b> <u>{city_model.temperature.comfort.min.c}°С</u>|<u>{city_model.temperature.comfort.max.c}</u>°С\n'
        f'♒<b>Влажность:</b> <u>{city_model.humidity.percent.min}%</u>|<u>{city_model.humidity.percent.max}%</u>\n'
        
        f'💨<b>Ветер:</b>\n'
        f'Min: <u>{SCALE_8.get(city_model.wind.direction.min.scale_8, "🟦нет данных ")}</u> | <u>{city_model.wind.speed.min.m_s} м/с</u>\n'
        f'Max: <u>{SCALE_8.get(city_model.wind.direction.max.scale_8, "🟦нет данных ")}</u> | <u>{city_model.wind.speed.max.m_s} м/с</u>\n'
        
        f'☔<b>Осадки:</b> {STORM.get(city_model.storm)}'
        f'{PRECIPITATION["INTENSITY"].get(city_model.precipitation.intensity)} '
        f'{PRECIPITATION["TYPE"].get(city_model.precipitation.type)} {city_model.precipitation.amount} мм\n'
        f'🌪️<b>Погодное явление:</b> {PHENOMENON.get(city_model.phenomenon)}\n'
        
        f'🧲<b>Геомагнитное поле:</b> <u>{GM.get(city_model.gm, "нет данных")}</u>\n'
    )
