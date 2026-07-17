from dataclasses import dataclass


@dataclass
class Character:
    id: int
    name: str
    category: str
    attributes: dict[str, bool]

