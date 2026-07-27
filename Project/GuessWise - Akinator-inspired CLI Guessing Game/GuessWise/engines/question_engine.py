"""
Question Engine

Responsible for managing
the remaining questions.
"""

from models.question import Question


class QuestionEngine:
    """Stores and manages remaining questions."""

    def __init__(self, questions: list[Question]):
        self.questions = questions.copy()

    def remaining(self) -> list[Question]:
        """Return all remaining questions."""
        return self.questions

    def remove(self, question: Question):
        """Remove a question after it has been asked."""
        if question in self.questions:
            self.questions.remove(question)

    def finished(self) -> bool:
        """Return True if there are no more questions."""
        return len(self.questions) == 0

    def count(self) -> int:
        """Return number of remaining questions."""
        return len(self.questions)

    def reset(self, questions: list[Question]):
        """Reset the question list."""
        self.questions = questions.copy()