class BotPhrase:
    """заготовленные ответы бота"""

    def command_only_pm(self) -> str:
        return "Команда доступна только в приватных сообщениях"

    def new_poll_saved(self) -> str:
        return "Опрос сохранен"

    def no_such_poll(self, poll_question) -> str:
        phrase = f"Опрос '{poll_question}' отсутствует в базе"
        return phrase

    def poll_sent(self) -> str:
        return "Опрос отправлен"

    def poll_question_exist(self) -> str:
        return "Опрос с такой темой уже существует!"

    def poll_deleted(self) -> str:
        return "Опрос удален"

    def no_saved_polls(self) -> str:
        return "Нет сохраненных опросов"

    def select_poll(self) -> str:
        return "Выберите нужный опрос"

    def select_action(self) -> str:
        return "Выберите действие"

    def no_chats(self) -> str:
        return "Групповые чаты с ботом отсутствуют"
