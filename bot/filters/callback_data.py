from aiogram.filters.callback_data import CallbackData


class CancelCallbackData(CallbackData, prefix="cancel_state"):
    pass


class CityCallbackData(CallbackData, prefix="city"):
    city_id: int
    city_name: str


class WeatherDayCallbackData(CallbackData, prefix="weather_day"):
    city_id: int
    day_number: int
