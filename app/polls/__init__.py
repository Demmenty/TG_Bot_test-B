from aiogram import Dispatcher

from app.bot.commands import COMMANDS
from main import config_path
from .accessor import DatabaseAccessor
from .commands import commands
from .config import setup_config
from .keyboards import BotKeyboard
from .phrases import BotPhrase


config = setup_config(config_path)

db = DatabaseAccessor(config)

phrases = BotPhrase()

keyboards = BotKeyboard()


async def setup_polls_module(dispatcher: Dispatcher):
    """подготавливает модуль к работе"""

    await db.create_tables()

    COMMANDS.update(commands)
