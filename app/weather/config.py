from dataclasses import dataclass
import yaml


@dataclass
class OpenWeatherConfig:
    api_key: str = None


@dataclass
class Config:
    weather: OpenWeatherConfig = None


def setup_config(config_path) -> Config:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    config = Config()

    config.weather = OpenWeatherConfig(
        api_key=raw_config["openweather"]["api_key"],
    )

    return config
