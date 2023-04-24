from dataclasses import dataclass


@dataclass
class BotCommand:
    name: str
    description: str
    usage: str = ""


@dataclass
class ExchangeConfig:
    api_key: str = None


@dataclass
class ConvertationRequest:
    from_currency: str
    to_currency: str
    amount: str


@dataclass
class ConvertationResponse:
    from_currency: str
    to_currency: str
    amount: int | float
    result: int | float
