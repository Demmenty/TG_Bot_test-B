import logging
from pathlib import Path
from aiogram import Dispatcher
from aiogram.utils import executor

from app.bot import dp


logging.basicConfig(level=logging.INFO)

config_path = Path(__file__).parent / "config.yml"


# настройка модулей перед запуском
async def on_startup(dispatcher: Dispatcher):
    from app.bot import setup_bot
    from app.exchange import setup_exchange_module
    from app.polls import setup_polls_module
    from app.random_animal import setup_animal_module
    from app.weather import setup_weather_module

    from app.bot.commands import COMMANDS, setup_commands

    await setup_bot(dispatcher)
    await setup_weather_module(dispatcher)
    await setup_exchange_module(dispatcher)
    await setup_animal_module(dispatcher)
    await setup_polls_module(dispatcher)

    await setup_commands(dispatcher, COMMANDS)


# точка входа
# подключаем все обработчики и запускаем цикл
if __name__ == "__main__":
    from app.bot import handlers
    from app.exchange import handlers
    from app.polls import handlers
    from app.random_animal import handlers
    from app.weather import handlers

    executor.start_polling(dp, on_startup=on_startup)
