from database.database import Base, engine

# Import all models so SQLAlchemy knows about them
from database.models import (
    Character,
    Attribute,
    CharacterAttribute,
    Question
)


def create_tables():
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully!")


if __name__ == "__main__":
    create_tables()