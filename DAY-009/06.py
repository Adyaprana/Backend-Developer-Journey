print("--------------sorted----------------")
# sorted() -->sorts data.

# Simple Sort
numbers = [5,1,8,2]
print(sorted(numbers))

# Descending
print(sorted(numbers,reverse=True))

# sorted() --> with key argument
words = [
    "python",
    "go",
    "javascript"
]
print(sorted(words,key=len))
print(sorted(words,key=len))

# Sort By Last Character:
words = [
    "apple",
    "cat",
    "dog"
]
print(
    sorted(
        words,
        key=lambda x: x[-1]
    )
)

# Backend Example --> Sort Users By Age
users = [
    {"name":"A","age":30},
    {"name":"B","age":20},
    {"name":"C","age":25}
]
print(sorted(users,key=lambda x: x["age"]))