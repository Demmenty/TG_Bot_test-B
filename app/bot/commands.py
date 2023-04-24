from aiogram import types
from aiogram.dispatcher import Dispatcher

from app.bot.dataclasses import BotCommand

# основные команды, модульные будут обновлять словарь
COMMANDS = {
    "start": BotCommand(
        name="start",
        description="Приветствие.",
    ),
    "help": BotCommand(
        name="help",
        description="Подробное описание функций.",
    ),
}


# установка подсказок в чате о доступных командах бота
async def setup_commands(dp: Dispatcher, commands: dict):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command=cmd.name, description=cmd.description)
            for cmd in commands.values()
        ]
    )
