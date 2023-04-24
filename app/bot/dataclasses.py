from dataclasses import dataclass


@dataclass
class BotCommand:
    name: str
    description: str
    usage: str = ""


@dataclass
class Chat:
    tg_id: int
    title: str
    id: int = None
