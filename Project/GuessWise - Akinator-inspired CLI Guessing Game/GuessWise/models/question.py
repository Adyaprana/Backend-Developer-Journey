from dataclasses import dataclass


@dataclass
class Question:
    id: int
    text: str
    attribute: str