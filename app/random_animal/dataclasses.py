from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    api_key: str = None


@dataclass
class TheCatApiConfig:
    api_key: str = None


@dataclass
class AnimalRequest:
    type: str = ""
