from dataclasses import dataclass
import yaml


@dataclass
class BotConfig:
    token: str = None


@dataclass
class DatabaseConfig:
    type: str = None
    name: str = None


@dataclass
class Config:
    bot: BotConfig = None
    db: DatabaseConfig = None


config = Config()


def setup_config(config_path) -> Config:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    config.bot = BotConfig(
        token=raw_config["bot"]["token"],
    )
    config.db = DatabaseConfig(
        type=raw_config["database"]["type"],
        name=raw_config["database"]["name"],
    )

    return config
