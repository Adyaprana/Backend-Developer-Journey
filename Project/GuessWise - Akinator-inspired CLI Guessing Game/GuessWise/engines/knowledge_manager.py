"""
Knowledge Manager

Responsible for selecting
the best next question.

The Game never decides
which question to ask.
"""


from engines.character_engine import CharacterEngine
from engines.question_engine import QuestionEngine
from models.question import Question


class KnowledgeManager:
    """Chooses the best question."""

    def __init__(
        self,
        character_engine: CharacterEngine,
        question_engine: QuestionEngine
    ):
        self.character_engine = character_engine
        self.question_engine = question_engine

    def best_question(self) -> Question:
        """Choose the best remaining question."""

        characters = self.character_engine.remaining()
        questions = self.question_engine.remaining()

        best_question = None
        best_score = float("inf")

        for question in questions:

            true_count = 0
            false_count = 0

            for character in characters:
                value = character.attributes.get(
                    question.attribute,
                    False
                )

                if value:
                    true_count += 1
                else:
                    false_count += 1
            
            if true_count == 0 or false_count == 0:
                continue
            score = abs(true_count - false_count)

            if score < best_score:
                best_score = score
                best_question = question

        if best_question:
            self.question_engine.remove(best_question)

        return best_question



    def process_answer(
        self,
        question: Question,
        answer: str
    ):
        """Process the user's answer."""

        if answer == "1":
            self.character_engine.filter(
                question.attribute,
                True
            )

        elif answer == "2":
            self.character_engine.filter(
                question.attribute,
                False
            )
        else:
            pass