"""
Character Engine

Responsible for:
- Storing candidates
- Filtering candidates
- Returning remaining candidates
"""

from models.character import Character


class CharacterEngine:
    """Handles all character filtering."""

    def __init__(self, characters: list[Character]):
        self.characters = characters

    def remaining(self) -> list[Character]:
        """Return all remaining candidates."""
        return self.characters

    def filter(self, attribute: str, expected_value: bool):
        """Filter candidates by attribute."""
        self.characters = [
            character
            for character in self.characters
            if character.attributes.get(attribute, False) == expected_value
        ]

    def count(self) -> int:
        """Return the number of remaining candidates."""
        return len(self.characters)

    def has_guess(self) -> bool:
        """Return True if exactly one candidate remains."""
        return len(self.characters) == 1

    def guess(self) -> Character:
        """Return the final guessed character."""
        return self.characters[0]