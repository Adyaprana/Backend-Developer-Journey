# List (A List stores multiple values in one variable.)
# A list is an ordered, mutable collection used to store multiple values.

# Imagine storing marks.
# Without List:
mark1 = 90
mark2 = 80
mark3 = 75
mark4 = 88

# Using List:
marks = [90, 80, 75, 88]

# Creating Lists: 

# Integer List
numbers = [90, 80,70,60,50]

# String List
names = ["Adyaprana", "Hari", "Ram","Shiv" ]

# Mixed List
data = ["python", 3.14, 100, True ] 

# Indexing (Every element has a position.)
names = ["A", "B", "C"]
#   A -> 0
#   B -> 1
#   C -> 2

language = ["python", "java", "go", "c++", "c" ]
print(language[0])

# Negative Indexing
language = ["python", "java", "go", "c++", "c" ]
print(language[-1])

language = ["python", "java", "go", "c++", "c" ]
print(language[0]) # also -5
print(language[1]) # also -4
print(language[2]) # also -3
print(language[3]) # also -2
print(language[4]) # also -1

# Slicing (Get multiple items.)
# list[start:end]
numbers = [1,2,3,4,5]
print(numbers[1:4])
print(numbers[:3])
print(numbers[2:])
print(numbers[::-1])


# Nested Lists
matrix = [
    [1,2,3],
    [4,5,6]
]
print(matrix)

# Used in:

# Tables
# Grids
# Data processing


# Copying Lists
# Bad
a = [1,2,3]
b = a
# Both point to same list.

# Good
b = a.copy()