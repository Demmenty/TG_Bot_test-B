from dataclasses import dataclass
import yaml


@dataclass
class ExchangeRates:
    api_key: str = None


@dataclass
class Config:
    exchange: ExchangeRates = None


def setup_config(config_path) -> Config:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    config = Config()

    config.exchange = ExchangeRates(
        api_key=raw_config["exchangerates"]["api_key"],
    )

    return config
