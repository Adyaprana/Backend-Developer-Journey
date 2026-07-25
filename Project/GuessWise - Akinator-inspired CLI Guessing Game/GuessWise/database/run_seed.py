from database.database import Base, engine
from database.models import (
    Character,
    Attribute,
    CharacterAttribute,
    Question
)
from database.seed import Seeder


def main():
    print("Creating database tables...")

    Base.metadata.create_all(engine)

    print("Seeding database...")

    seeder = Seeder()
    seeder.seed()

    print("✅ Database setup completed successfully!")


if __name__ == "__main__":
    main()