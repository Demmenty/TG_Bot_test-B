from aiogram import types

from main import dp
from . import phrases, service, db
from .exception import WeatherException


@dp.message_handler(commands=["weather"])
async def send_weather(msg: types.Message):
    """выдает инфо о погоде"""

    request = service.prepare_request(msg)

    # если юзер не указал город
    if not request.city_query:
        # проверяем есть ли инфо о последнем запрошенном им городе в бд
        request = await db.get_usercity(request)

        if not request.city_query:
            await msg.answer(phrases.invalid_request("weather"))
            return
        
        # и делаем запрос по нему
        response = await service.get_weather(request)
        await msg.answer(phrases.weather_response(response))
        return
        
    try:
        response = await service.get_weather(request)
        await msg.answer(phrases.weather_response(response))
        # если юзер указал город и все прошло ок, сохраняем в бд
        await db.save_usercity(request)

    except WeatherException as error:
        await msg.answer(error)
