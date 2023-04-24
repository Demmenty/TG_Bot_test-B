from datetime import datetime

from .commands import commands
from .dataclasses import WeatherResponse


class BotPhrase:
    """заготовленные ответы бота"""

    def weather_response(self, weather: WeatherResponse) -> str:
        phrase = (
            f"В городе {weather.city} ({weather.country}) сегодня {weather.description}.\n\n"
            f"Температура воздуха {weather.temp}°C, ощущается как {weather.feels_like}°C\n"
            f"Атмосферное давление {round(weather.pressure * 0.75)} мм рт.ст.\n"
            f"Влажность {weather.humidity} %\n"
            f"Ветер {weather.wind_speed} м/с\n"
            f"Облачность {weather.clouds} %\n\n"
            f"Информация для вампиров:\n"
            f"восход солнца - {datetime.utcfromtimestamp(weather.sunrise).strftime('%H:%M')}, "
            f"закат - {datetime.utcfromtimestamp(weather.sunset).strftime('%H:%M')}."
        )
        return phrase

    def invalid_request(self, command: str) -> str:
        phrase = "Неверный запрос.\n\n" + commands[command].usage
        return phrase
