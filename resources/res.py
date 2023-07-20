from pygismeteo_base import models

COMMANDS_FOR_GET_WEATHER = '''
{city_name}
Сегодня:
/weather_{city_id}_1x1
Сегодня шаг 3 часа:
/weather_{city_id}_3x1
3 дня шаг 6 часов:
/weather_{city_id}_6x3
3 дня шаг 24 часа:
/weather_{city_id}_24x3
10 дней шаг 24 часа:
/weather_{city_id}_24x10
Определённый день
/days_{city_id}
'''

COMMANDS_FOR_GET_DAYS = '''
{}
/day_{city_id}_1
{}
/day_{city_id}_2
{}
/day_{city_id}_3
{}
/day_{city_id}_4
{}
/day_{city_id}_5
{}
/day_{city_id}_6
{}
/day_{city_id}_7
{}
/day_{city_id}_8
{}
/day_{city_id}_9
{}
/day_{city_id}_10
'''
