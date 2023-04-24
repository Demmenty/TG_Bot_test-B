from dataclasses import dataclass
import yaml


@dataclass
class OpenAI:
    api_key: str = None


@dataclass
class TheCatApi:
    api_key: str = None


@dataclass
class Config:
    openai: OpenAI = None
    thecatapi: TheCatApi = None


def setup_config(config_path) -> Config:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    config = Config()

    config.openai = OpenAI(
        api_key=raw_config["openai"]["api_key"],
    )
    config.thecatapi = TheCatApi(
        api_key=raw_config["thecatapi"]["api_key"],
    )

    return config
