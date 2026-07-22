import json

from models.character import Character
from models.question import Question
from repository.repository import Repository


class JsonRepository(Repository):

    def get_characters(self) -> list[Character]:
        with open("data/characters.json", "r") as file:
            data = json.load(file)
            characters = []
            for item in data:
                character = Character(**item)
                characters.append(character)
            return characters
            
    def get_questions(self) -> list[Question]:
        with open("data/questions.json", "r") as file:
            data = json.load(file)

            questions = []
            for group in data:
                category = group["category"]

                for item in group["questions"]:
                    questions.append(
                        Question(
                            id=item["id"],
                            category=category,
                            text=item["text"],
                            attribute=item["attribute"]
                        )
                    )
            return questions








