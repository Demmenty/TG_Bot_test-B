from aiogram import Dispatcher

from app.bot.commands import COMMANDS
from main import config_path
from .commands import commands
from .config import setup_config
from .phrases import BotPhrase
from .service import RandomAnimalService


config = setup_config(config_path)

service = RandomAnimalService()

phrases = BotPhrase()


async def setup_animal_module(dispatcher: Dispatcher):
    """подготавливает модуль к работе"""

    await service.connect(config)

    COMMANDS.update(commands)
