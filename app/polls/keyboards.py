from aiogram import types

from .dataclasses import Poll


class BotKeyboard:
    """заготовленные клавиатуры для бота"""

    def polls_menu(self) -> types.ReplyKeyboardMarkup:
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        keyboard.add(
            types.KeyboardButton(
                text="Создать опрос",
                request_poll=types.KeyboardButtonPollType(
                    type=types.PollType.REGULAR
                ),
            )
        )
        keyboard.add("Сохраненные опросы")
        keyboard.add("Отмена")

        return keyboard

    def polls_list(self, saved_polls: list[Poll]) -> types.ReplyKeyboardMarkup:
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        for poll in saved_polls:
            keyboard.add(f"Опрос '{poll.question}'")
        keyboard.add("Отмена")

        return keyboard

    def poll_menu(self, poll: Poll) -> types.ReplyKeyboardMarkup:
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        keyboard.add(f"Отправить в чаты опрос '{poll.question}'")
        keyboard.add(f"Удалить опрос '{poll.question}'")
        keyboard.add("Отмена")

        return keyboard
