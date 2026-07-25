from repository.postgres_repository import PostgresRepository
from engines.character_engine import CharacterEngine
from engines.question_engine import QuestionEngine


class Game:
    def __init__(self):
        self.repository = PostgresRepository()

    def start(self):
        self.all_characters = self.repository.get_characters()
        self.questions = self.repository.get_questions()

        print("Game Started")
        print(f"Loaded {len(self.all_characters)} characters")
        print(f"Loaded {len(self.questions)} questions")

        self.show_menu()
        
    
    def show_menu(self):
        while True:
            print("===================================")
            print("        🎯 GuessWise               ")
            print("===================================")

            print("1. Character")
            print("2. Animal")
            print("3. Object")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ").strip()
            if choice == "1":
                self.select_category("character")
                self.play_game()

            elif choice == "2":
                self.select_category("animal")
                self.play_game()

            elif choice == "3":
                self.select_category("object")
                self.play_game()

            elif choice == "4":
                print("Game Exit")
                break
            else:
                print("Invalid choice! Please enter a number from 1 to 4.")
                continue

    def play_game(self):
        
        while True:
            if self.question_engine.finished():
                print("🤔 I couldn't uniquely identify your answer.")
                print("\nPossible Matches:")
                print("\nRemaining Candidates:")
                for character in self.character_engine.remaining():
                    print("-", character.name)

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

            print("\n=========================")
            print("🎯 GuessWise")
            print("=========================")
            print(f"Category : {self.current_category.title()}")
            print(f"Remaining Candidates : {self.character_engine.count()}")
            
            print(f"Question {self.question_engine.question_number()}")
            question = self.question_engine.current_question()
            print(question.text)
            print("1. Yes")
            print("2. No")
            print("3. Probably")
            print("4. Probably Not")
            print("5. Don't Know")
            answers = {
                "1": "Yes",
                "2": "No",
                "3": "Probably",
                "4": "Probably Not",
                "5": "Don't Know"
            }
            choice = input("Enter your choice (1-5): ").strip()
            


            if choice == "1":
                self.character_engine.filter(
                    question.attribute,
                    True
                )

            elif choice == "2":
                self.character_engine.filter(
                    question.attribute,
                    False
                )              

            elif choice in ["3", "4", "5"]:
                print(f"You selected: {answers[choice]}")
            else:
                print("Invalid choice! Please enter a number from 1 to 5.")

            print("\nRemaining Candidates:")
            for character in self.character_engine.remaining():
                print("-", character.name)

            if self.character_engine.has_guess():
                print("\n🎉 I guessed your answer!")
                guess = self.character_engine.guess()
                print(f"It's: {guess.name}")

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return
            
            elif self.character_engine.count() == 0:
                print("\n❌ No matching character found.")
                
                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return
            self.question_engine.next_question()






    def select_category(self, category: str):
        self.current_category = category

        characters = [
            character
            for character in self.all_characters
                if character.category == category
        ]
        self.character_engine = CharacterEngine(characters)

        questions = [
            question
            for question in self.questions
            if question.category == category
        ]
        self.question_engine = QuestionEngine(questions)


    def play_again(self) -> bool:
        while True:
            print("\n-----------------------")
            print("Play Again?")
            print("-----------------------")
            print("1. Yes")
            print("2. No")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                return True

            elif choice == "2":
                return False
            print("Invalid choice!")