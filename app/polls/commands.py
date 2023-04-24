from app.bot.dataclasses import BotCommand


commands = {
    "poll": BotCommand(
        name="poll",
        description="Команда управления опросами.",
        usage="Недоступна для использования в чатах!",
    ),
}
