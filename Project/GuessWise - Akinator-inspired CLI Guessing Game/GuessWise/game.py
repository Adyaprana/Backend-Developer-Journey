from repository.json_repository import JsonRepository

class Game:
    def __init__(self):
        self.repository = JsonRepository()
    def start(self):
        self.all_characters = self.repository.get_characters()
        self.characters = self.all_characters.copy()
        self.questions = self.repository.get_questions()
        
        print("Game Started")
        print(f"Loaded {len(self.characters)} characters")
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
        
        question_index = 0
        while True:
            if question_index >= len(self.current_questions):
                print("🤔 I couldn't uniquely identify your answer.")
                print("\nPossible Matches:")
                self.show_remaining_candidates()

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return

            print("\n=========================")
            print("🎯 GuessWise")
            print("=========================")
            print(f"Category : {self.current_category.title()}")
            print(f"Remaining Candidates : {len(self.characters)}")
            
            print(f"Question {question_index + 1}")
            question = self.current_questions[question_index]
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
                self.filter_characters(question.attribute, True)

            elif choice == "2":
                self.filter_characters(question.attribute, False)               

            elif choice in ["3", "4", "5"]:
                print(f"You selected: {answers[choice]}")
            else:
                print("Invalid choice! Please enter a number from 1 to 5.")

            self.show_remaining_candidates()

            if len(self.characters) == 1:
                print("\n🎉 I guessed your answer!")
                print(f"It's: {self.characters[0].name}")

                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return
            
            elif len(self.characters) == 0:
                print("\n❌ No matching character found.")
                
                if self.play_again():
                    self.select_category(self.current_category)
                    return self.play_game()
                return
            question_index += 1






    def select_category(self, category: str):
        self.current_category = category

        self.characters = [
            character
            for character in self.all_characters
            if character.category == category
        ]

        self.current_questions = [
            question
            for question in self.questions
            if question.category == category
        ]

    def filter_characters(self, attribute: str, expected_value: bool):
        self.characters = [
            character
            for character in self.characters
            if character.attributes.get(attribute, False) == expected_value
        ]

    def show_remaining_candidates(self):
        print("\nRemaining Candidates:")
        for character in self.characters:
            print("-", character.name)

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