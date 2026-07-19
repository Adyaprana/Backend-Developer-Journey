from repository.json_repository import JsonRepository

class Game:
    def __init__(self):
        self.repository = JsonRepository()
    def start(self):
        self.characters = self.repository.get_characters()
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
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice == "1":
                self.character_mode()

            elif choice == "2":
                print("Animal Mode")
                pass

            elif choice == "3":
                print("Object Mode")
                pass

            elif choice == "4":
                print("Game Exit")
                break
            else:
                print("Invalid choice! Please enter a number from 1 to 4.")
                continue

    def character_mode(self):
        while True:
            print("\n=========================")
            print("Character Mode")
            print("=========================")
            print("\nQuestion 1\n")
            question = self.questions[0]
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
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice in ["1", "2", "3", "4", "5"]:
                print(f"You selected: {answers[choice]}")
                break 
            else:
                print("Invalid choice! Please enter a number from 1 to 5.")
