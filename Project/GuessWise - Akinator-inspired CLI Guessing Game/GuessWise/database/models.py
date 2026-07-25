from sqlalchemy import (
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.database import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    category: Mapped[str] = mapped_column(String(50))

    attributes: Mapped[list["CharacterAttribute"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan"
    )


class Attribute(Base):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    questions: Mapped[list["Question"]] = relationship(
        back_populates="attribute"
    )

    characters: Mapped[list["CharacterAttribute"]] = relationship(
        back_populates="attribute"
    )


class CharacterAttribute(Base):
    __tablename__ = "character_attributes"

    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        primary_key=True
    )

    attribute_id: Mapped[int] = mapped_column(
        ForeignKey("attributes.id"),
        primary_key=True
    )

    value: Mapped[bool] = mapped_column(Boolean)

    character: Mapped["Character"] = relationship(
        back_populates="attributes"
    )

    attribute: Mapped["Attribute"] = relationship(
        back_populates="characters"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)

    category: Mapped[str] = mapped_column(String(50))

    text: Mapped[str] = mapped_column(String(255))

    attribute_id: Mapped[int] = mapped_column(
        ForeignKey("attributes.id")
    )

    attribute: Mapped["Attribute"] = relationship(
        back_populates="questions"
    )