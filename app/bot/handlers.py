from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotKicked

from app.bot.dataclasses import Chat
from . import db, dp, phrases


@dp.message_handler(commands=["start"])
async def handle_start(msg: types.Message):
    """приветствует и описывает доступные функции"""

    await msg.answer(phrases.start_msg(msg.from_user.first_name))


@dp.my_chat_member_handler()
async def reqister_chat(msg: types.Message):
    """записывает в базу id нового чата"""

    # не реагируем на лички
    if msg.chat.type == "private":
        return

    # не реагируем на кики
    if msg.new_chat_member.status == "left":
        return

    chat = Chat(
        tg_id=msg.chat.id,
        title=msg.chat.title,
    )
    # проверяем на наличие в базе
    chat_exist = await db.is_chat_exist(chat)

    # если в базе нет - сохраняем
    if not chat_exist:
        await db.add_chat(chat)


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def welcome_new_member(msg: types.Message):
    """приветствует нового члена или чат, предлагает узнать о функциях"""

    await msg.reply(phrases.welcome_new_member(msg.from_user.first_name))


@dp.message_handler(commands=["help"])
async def send_help(msg: types.Message):
    """подробно описывает доступные функции"""

    await msg.answer(phrases.bot_help())


@dp.message_handler(Text(equals="Отмена"))
async def remove_keyboard(msg: types.Message):
    """скрывает клавиатуру"""

    await msg.answer(phrases.cancel(), reply_markup=types.ReplyKeyboardRemove())
