from dataclasses import dataclass

@dataclass
class Question:
    id: int
    category: str
    text: str
    attribute: str