from dataclasses import dataclass


@dataclass
class WeatherRequest:
    city: str
    country: str = ""
    state: str = ""

    @property
    def as_query(self):
        """возвращает строку из значений атрибутов через запятую"""

        return ",".join([val for val in self.__dict__.values() if val])


@dataclass
class WeatherResponse:
    city: str
    country: str
    description: str
    temp: int
    feels_like: int
    pressure: int
    humidity: int
    wind_speed: float
    clouds: int
    sunrise: int
    sunset: int
