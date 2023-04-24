import random
from aiogram import types

from main import dp
from . import phrases, service


@dp.message_handler(commands=["animal"])
async def send_random_animal(msg: types.Message):
    """показывает случайную картинку с животными"""

    request = service.prepare_request(msg.text)

    services = {
        "рисунок": service.paint_pic,
        "кошка": service.get_cat,
        "кошара": service.get_bigcat,
        "собака": service.get_dog,
        "лиса": service.get_fox,
    }

    # выбираем из доступных сервисов по типу запроса
    target_service = services.get(request.type)

    # либо рандомный
    if not target_service:
        target_service = random.choice(list(services.values()))

    pic_url = await target_service()

    # бывает, что сервисы отключаются
    if not pic_url:
        await msg.reply(phrases.service_unavailable())
        return

    await msg.answer_photo(pic_url)
