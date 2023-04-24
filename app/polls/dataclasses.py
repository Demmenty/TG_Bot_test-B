from dataclasses import dataclass


@dataclass
class Poll:
    question: str
    options: list[str]
    type: str = "regular"
    is_anonymous: bool = False
    multiple_answers: bool = False
