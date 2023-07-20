from aiogram.filters import Filter
from aiogram.types import Message


class CMDWeatherFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return 'weather' in message.text[1:].split('_')


class CMDWeatherDaysFilter(Filter):
    async def __call__(self, message: Message, *args, **kwargs) -> bool:
        return 'days' in message.text[1:].split('_')
