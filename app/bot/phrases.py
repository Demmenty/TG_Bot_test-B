from .commands import COMMANDS


class BotPhrase:
    """заготовленные ответы бота"""

    def start_msg(self, user: str) -> str:
        phrase = (
            f"Хай, {user}! Я самый лучший телеграм-бот!\n\n"
            "Вот список моих возможностей:\n"
        )

        for command in COMMANDS.values():
            if command.name in ("start", "help"):
                continue

            command_repr = f"/{command.name}\n" f"{command.description}\n"
            phrase += "\n" + command_repr

        phrase += "\nБолее подробное описание доступно по команде /help"

        return phrase

    def welcome_new_member(self, user: str) -> str:
        phrase = (
            f"Приветствую, {user}!\n"
            "Если хотите ознакомиться с моими возможностями, используйте /help :)"
        )

        return phrase

    def bot_help(self) -> str:
        phrase = "Доступные команды:\n\n"

        for command in COMMANDS.values():
            command_help = (
                f"/{command.name}\n"
                f"{command.description}\n"
                f"{command.usage}\n"
            )
            phrase += command_help

        return phrase

    def cancel(self) -> str:
        return "Галя, у нас отмена!"
