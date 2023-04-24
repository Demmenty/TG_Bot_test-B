from aiogram import types

from . import phrases


def pm_only(handler):
    """отменяет выполнение, если сообщение пришло не в личке"""

    async def wrapper(msg: types.Message):

        if msg.chat.type in ("group", "supergroup"):

            if msg.text.startswith("/poll"):
                await msg.reply(phrases.command_only_pm())

            return

        return await handler(msg)

    return wrapper
