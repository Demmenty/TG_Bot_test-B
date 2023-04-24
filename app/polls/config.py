from dataclasses import dataclass
import yaml


@dataclass
class DatabaseConfig:
    type: str = None
    name: str = None


@dataclass
class Config:
    db: DatabaseConfig = None


def setup_config(config_path) -> Config:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    config = Config()

    config.db = DatabaseConfig(
        type=raw_config["database"]["type"],
        name=raw_config["database"]["name"],
    )

    return config
