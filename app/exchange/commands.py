from .dataclasses import BotCommand


commands = {
    "convert": BotCommand(
        name="convert",
        description="Команда для конвертации валют.",
        usage="Необходимо передать трехбуквенный код валют и сумму.\n"
        "Формат: /convert <сумма> <валюта> <желаемая_валюта>\n"
        "Пример: /convert 100 USD RUB\n",
    ),
}
