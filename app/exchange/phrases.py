from .commands import commands
from .dataclasses import ConvertationResponse


class BotPhrase:
    """заготовленные ответы бота"""

    def convertation_response(self, convertation: ConvertationResponse) -> str:
        phrase = (
            f"{convertation.amount} {convertation.from_currency}  =  "
            f"{convertation.result} {convertation.to_currency}"
        )
        return phrase

    def invalid_request(self, command: str) -> str:
        phrase = "Неверный запрос.\n\n" + commands[command].usage
        return phrase
