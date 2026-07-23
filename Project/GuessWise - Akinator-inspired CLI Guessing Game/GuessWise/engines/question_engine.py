"""
Question Engine

Responsible for question navigation.

Responsibilities:
- Store questions.
- Return the current question.
- Move to the next question.
- Reset question order.

The Game class should never manage question indexes directly.
"""

from models.question import Question


class QuestionEngine:
    """Handles question navigation."""

    def __init__(self, questions: list[Question]):
        self.questions = questions
        self.current_index = 0

    def current_question(self) -> Question:
        """Return the current question."""
        return self.questions[self.current_index]

    def next_question(self):
        """Move to the next question."""
        self.current_index += 1

    def reset(self):
        """Reset to the first question."""
        self.current_index = 0

    def finished(self) -> bool:
        """Return True if there are no more questions."""
        return self.current_index >= len(self.questions)

    def question_number(self) -> int:
        """Return the current question number (1-based)."""
        return self.current_index + 1