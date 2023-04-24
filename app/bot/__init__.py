from aiogram import types, Bot, Dispatcher
from pathlib import Path

from .accessor import DatabaseAccessor
from .config import setup_config
from .phrases import BotPhrase


config_path = Path(__file__).parent.parent.parent / "config.yml"

# создание экземляров всего, что нужно, и настройка
config = setup_config(config_path)

bot = Bot(token=config.bot.token)

dp = Dispatcher(bot)

db = DatabaseAccessor(config)

phrases = BotPhrase()

admin_rights = types.ChatAdministratorRights(
    can_manage_chat=True, can_delete_messages=True
)

async def setup_bot(dispatcher: Dispatcher):
    """подготавливает бота к работе"""

    # создаем таблицы в бд
    await db.create_tables()
    # устанавливаем желаемые права бота по умолчанию
    await bot.set_my_default_administrator_rights(admin_rights)
