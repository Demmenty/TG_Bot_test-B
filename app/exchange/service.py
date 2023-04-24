from logging import getLogger
from typing import Optional
from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from .config import Config
from .dataclasses import ConvertationRequest, ConvertationResponse
from .exception import ConvertationException


class ExchangeService:
    """сервис доступа к стороннему api курса валют"""

    def __init__(self):
        self.logger = getLogger("ExchangeService")
        self.session: Optional[ClientSession] = None
        self.api_key: Optional[str] = None
        self.host: str = "https://api.apilayer.com/exchangerates_data/"

    async def connect(self, config: Config):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.api_key = config.exchange.api_key

    def prepare_request(self, msg_text: str) -> ConvertationRequest | None:
        """подготавливает текст сообщения с командой к обработке"""

        msg_text_lst = [word.strip(" ,.!?;:") for word in msg_text.split(" ")]

        try:
            request = ConvertationRequest(
                amount=msg_text_lst[1],
                from_currency=msg_text_lst[2],
                to_currency=msg_text_lst[3],
            )
            return request

        except Exception:
            return None

    def _build_url(self, method: str, params: dict) -> str:
        """строит путь для запроса к api сервиса по переданным параметрам"""

        url = (
            self.host + method + "?"
            + "&".join([f"{k}={v}" for k, v in params.items()])
        )

        return url

    async def convert_currency(
        self, request: ConvertationRequest
    ) -> ConvertationResponse:
        """конвертирует валюту и возвращает результат"""

        url = self._build_url(
            method="convert",
            params={
                "to": request.to_currency,
                "from": request.from_currency,
                "amount": request.amount,
                "apikey": self.api_key,
            },
        )

        async with self.session.get(url) as response:
            data = await response.json()

        if not data.get("success"):
            self.logger.info(data)
            raise ConvertationException(data["message"])

        response = ConvertationResponse(
            from_currency=data["query"]["from"],
            to_currency=data["query"]["to"],
            amount=data["query"]["amount"],
            result=data["result"],
        )
        return response
