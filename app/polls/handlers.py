from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotKicked

from main import dp
from . import db, keyboards, phrases
from .dataclasses import Poll
from .decorators import pm_only

# сложно было понять, как именно требуется осуществить функцию создания опросов
# по-хорошему, хочется добавить ещё аутентификацию админа, возможно API
# и сохранение результатов опросов в бд или файл (путем обработки types.PollAnswer)
# но времени просто не остается

@dp.message_handler(commands=["poll"])
@pm_only
async def show_polls_menu(msg: types.Message):
    """показывает меню управления опросами"""

    await msg.answer(
        phrases.select_action(), reply_markup=keyboards.polls_menu()
    )

@dp.message_handler(content_types=["poll"])
@pm_only
async def save_poll(msg: types.Message):
    """сохраняет отправленный опрос"""

    # не реагируем на викторины
    if msg.poll.type == "quiz":
        return

    new_poll = Poll(
        question=msg.poll.question,
        options=[option.text for option in msg.poll.options],
        is_anonymous=msg.poll.is_anonymous,
        multiple_answers=msg.poll.allows_multiple_answers,
    )

    # ограничение одинаковых вопросов
    poll_exist = await db.is_poll_exist(new_poll)

    if poll_exist:
        await msg.reply(phrases.poll_question_exist())
        return

    await db.save_poll(new_poll)
    await msg.answer(
        phrases.new_poll_saved(), reply_markup=keyboards.polls_menu()
    )


@dp.message_handler(Text(equals="Сохраненные опросы"))
@pm_only
async def show_polls(msg: types.Message):
    """предоставляет список сохраненных опросов"""

    saved_polls = await db.get_polls()

    if not saved_polls:
        await msg.answer(
            phrases.no_saved_polls(), reply_markup=keyboards.polls_menu()
        )
        return

    # высылаем клавиатуру с названиями опросов
    await msg.answer(
        phrases.select_poll(),
        reply_markup=keyboards.polls_list(saved_polls),
    )


@dp.message_handler(Text(startswith="Опрос"))
@pm_only
async def show_poll_menu(msg: types.Message):
    """показывает меню управления сохраненным опросом"""

    # отделяем название опроса от команды
    poll_question = msg.text.replace("Опрос", "").strip("' ")
    # находим соответствующий опрос в базе
    poll = await db.get_poll_by_question(poll_question)

    if not poll:
        await msg.reply(
            phrases.no_such_poll(poll_question),
            reply_markup=keyboards.polls_menu(),
        )
        return

    # предоставляем меню управления выбранным опросом
    await msg.reply(
        phrases.select_action(), reply_markup=keyboards.poll_menu(poll)
    )


@dp.message_handler(Text(startswith="Удалить опрос"))
@pm_only
async def delete_poll(msg: types.Message):
    """удаляет сохраненный опрос из базы"""

    poll_question = msg.text.replace("Удалить опрос", "").strip("' ")

    await db.delete_poll(poll_question)

    await msg.reply(phrases.poll_deleted(), reply_markup=keyboards.polls_menu())


@dp.message_handler(Text(startswith="Отправить в чаты опрос"))
@pm_only
async def send_poll(msg: types.Message):
    """отправляет опрос в чаты бота"""

    # отделяем название опроса от команды
    poll_question = msg.text.replace("Отправить в чаты опрос", "").strip("' ")
    # находим соответствующий опрос в базе
    poll = await db.get_poll_by_question(poll_question)

    if not poll:
        await msg.reply(
            phrases.no_such_poll(poll_question),
            reply_markup=keyboards.polls_menu(),
        )
        return

    # достаем инфо об известных чатах с нашим ботом
    chats = await db.get_chats()

    if not chats:
        await msg.reply(
            phrases.no_chats(), reply_markup=types.ReplyKeyboardRemove()
        )
        return

    # отправляем опрос в каждый чат
    for chat in chats:
        try:
            await msg.bot.send_poll(
                chat.tg_id,
                poll.question,
                poll.options,
                poll.is_anonymous,
                poll.type,
                poll.multiple_answers,
            )
        # чат мог остаться в базе, если бота кикнули - исправляем
        except BotKicked:
            await db.delete_chat(chat)

    # уведомляем об успешном успехе
    await msg.reply(phrases.poll_sent(), reply_markup=keyboards.polls_menu())
