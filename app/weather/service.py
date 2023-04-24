from logging import getLogger
from typing import Optional
from aiohttp import TCPConnector
from aiohttp.client import ClientSession
from aiogram import types

from .config import Config
from .dataclasses import WeatherRequest, WeatherResponse
from .exception import WeatherException


class WeatherService:
    """сервис доступа к стороннему api погоды"""

    def __init__(self):
        self.logger = getLogger("WeatherService")
        self.session: Optional[ClientSession] = None
        self.api_key: Optional[str] = None
        self.host: str = "https://api.openweathermap.org/data/2.5/"

    async def connect(self, config: Config):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.api_key = config.weather.api_key

    def prepare_request(self, msg: types.Message) -> WeatherRequest:
        """подготавливает текст сообщения с командой к обработке"""

        city_lst = msg.text.split(" ")[1:]
        city_query = ",".join([v.strip(" ,.!?;:'") for v in city_lst])

        request = WeatherRequest(
            user_id=msg["from"]["id"],
            city_query=city_query,
        )
        return request

    def _build_url(self, method: str, params: dict) -> str:
        """строит путь для запроса к api погоды по переданным параметрам"""

        url = (
            self.host + method + "?"
            + "&".join([f"{k}={v}" for k, v in params.items()])
        )

        return url

    async def get_weather(self, request: WeatherRequest) -> WeatherResponse:
        """возвращает данные о погоде в переданном городе"""

        url = self._build_url(
            method="weather",
            params={
                "q": request.city_query,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru",
            },
        )

        async with self.session.get(url) as response:
            data = await response.json()

        ok_status = 200
        if data["cod"] != ok_status:
            self.logger.info(data)
            raise WeatherException(data["message"])

        weather = WeatherResponse(
            city=data["name"],
            country=data["sys"]["country"],
            description=data["weather"][0]["description"],
            temp=round(data["main"]["temp"]),
            feels_like=round(data["main"]["feels_like"]),
            pressure=data["main"]["pressure"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
            clouds=data["clouds"]["all"],
            sunrise=data["sys"]["sunrise"],
            sunset=data["sys"]["sunset"],
        )

        return weather
