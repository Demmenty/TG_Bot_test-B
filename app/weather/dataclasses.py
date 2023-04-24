from dataclasses import dataclass


@dataclass
class WeatherRequest:
    user_id: int
    city_query: str = ""


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
