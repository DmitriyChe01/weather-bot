from aiogram.fsm.state import StatesGroup, State


class WeatherSearchStates(StatesGroup):
    input_city_name = State()
    choice_city_name = State()


