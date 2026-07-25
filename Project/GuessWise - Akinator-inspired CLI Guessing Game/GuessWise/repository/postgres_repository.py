from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import (
    Character as DBCharacter,
    Question as DBQuestion
)

from models.character import Character
from models.question import Question
from repository.repository import Repository

class PostgresRepository(Repository):

    def __init__(self):
        self.db: Session = SessionLocal()

    def get_characters(self) -> list[Character]:
        db_characters = (
            self.db.query(DBCharacter)
            .all()
        )

        characters = []

        for db_character in db_characters:

            # Convert database relationships back
            # into the dictionary used by the game.
            attributes = {}

            for character_attribute in db_character.attributes:
                attributes[
                    character_attribute.attribute.name
                ] = character_attribute.value

            game_character = Character(
                id=db_character.id,
                name=db_character.name,
                category=db_character.category,
                attributes=attributes
            )

            characters.append(game_character)

        return characters
    
    def get_questions(self) -> list[Question]:
        db_questions = (
            self.db.query(DBQuestion)
            .all()
        )
        questions = []
        for db_question in db_questions:

            game_question = Question(
                id=db_question.id,
                category=db_question.category,
                text=db_question.text,
                attribute=db_question.attribute.name
            )

            questions.append(game_question)

        return questions