from abc import ABC, abstractmethod

from models.character import Character
from models.question import Question


class Repository(ABC):

    @abstractmethod
    def get_characters(self) -> list[Character]:
        pass

    @abstractmethod
    def get_questions(self) -> list[Question]:
        pass