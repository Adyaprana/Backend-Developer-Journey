from repository.json_repository import JsonRepository

repository = JsonRepository()

characters = repository.get_characters()
questions = repository.get_questions()

print("Characters:")
for character in characters:
    print(character)

print("\nQuestions:")
for question in questions:
    print(question)