from aiogram import types

from main import dp
from . import phrases, service
from .exception import ConvertationException


@dp.message_handler(commands=["convert"])
async def send_convertation(msg: types.Message):
    """конвертирует валюту"""

    request = service.prepare_request(msg.text)

    # если неправильный запрос - реквест не получится
    if not request:
        await msg.answer(phrases.invalid_request("convert"))
        return

    try:
        response = await service.convert_currency(request)
        await msg.reply(phrases.convertation_response(response))

    except ConvertationException as error:
        await msg.answer(error)
