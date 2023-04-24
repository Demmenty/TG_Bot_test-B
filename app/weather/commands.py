from app.bot.dataclasses import BotCommand


commands = {
    "weather": BotCommand(
        name="weather",
        description="Команда получения текущей погоды.",
        usage="Необходимо передать название города.\n"
        "Для уточнения можно передать двухбуквенный код страны через пробел.\n"
        "Пример: /weather Москва US\n"
        "Если город не указан, выводится информация по последнему запрошенному.\n",
    )
}
