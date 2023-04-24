from aiogram import types

from main import dp
from . import phrases, service
from .exception import WeatherException


@dp.message_handler(commands=["weather"])
async def send_weather(msg: types.Message):
    """выдает инфо о погоде"""

    request = service.prepare_request(msg.text)

    # TODO добавить сохранение в кеш или бд {юзер: последний запрошенный город}
    # и если он не указал город в запросе, то выдается информация о последнем
    # если останется время

    if not request:
        await msg.answer(phrases.invalid_request("weather"))
        return

    try:
        response = await service.get_weather(request)
        await msg.answer(phrases.weather_response(response))

    except WeatherException as error:
        await msg.answer(error)
