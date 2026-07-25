import json

from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import (
    Character,
    Attribute,
    CharacterAttribute,
    Question
)

class Seeder:

    def __init__(self):
        self.db: Session = SessionLocal()

    def seed(self):
        self.seed_characters()
        self.seed_questions()

        self.db.commit()
        self.db.close()


        print("✅ Database Seeded Successfully")

    def seed_characters(self):

        with open("data/characters.json", "r") as file:
            data = json.load(file)

        for item in data:
            self.insert_character(item)
    
    def insert_character(self, item):

        character = Character(
            id=item["id"],
            name=item["name"],
            category=item["category"]
        )

        self.db.add(character)
        self.db.flush()

        self.insert_attributes(
            character.id,
            item["attributes"]
        )

    def insert_attributes(
        self,
        character_id,
        attributes
    ):
        for name, value in attributes.items():

            attribute = (
                self.db.query(Attribute)
                .filter_by(name=name)
                .first()
            )
            if attribute is None:
                attribute = Attribute(
                    name=name
                )
                self.db.add(attribute)
                self.db.flush()

            character_attribute = CharacterAttribute(
                character_id=character_id,
                attribute_id=attribute.id,
                value=value
            )

            self.db.add(character_attribute)


    def seed_questions(self):

        with open("data/questions.json", "r") as file:
            data = json.load(file)
        for group in data:
            category = group["category"]

            for item in group["questions"]:
                self.insert_question(
                    category,
                    item
                )
    
    def insert_question(
        self,
        category,
        item
    ):
        attribute = (
            self.db.query(Attribute)
            .filter_by(name=item["attribute"])
            .first()
        )

        if attribute is None:
            raise ValueError(
                f"Attribute '{item['attribute']}' not found."
            )

        question = Question(

            category=category,
            text=item["text"],
            attribute_id=attribute.id
        )

        self.db.add(question)
       