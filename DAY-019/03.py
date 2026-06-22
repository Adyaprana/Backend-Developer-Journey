# GENERATOR: Generator is a special function.
# Instead of: return
# it uses: yield

# Why Python Created Generators
# Normal function:
def get_numbers():
    return [1, 2, 3, 4, 5]
# Everything is created immediately.
# Memory used:
# 1
# 2
# 3
# 4
# 5
# all together.

# Generator:
def get_numbers():
    yield 1
    yield 2
    yield 3
# Creates values only when needed.

# return = Give Entire Box
# yield = Give One Item At A Time




# FIRST GENERATOR

def count():
    yield 1
    yield 2
    yield 3
gen = count()
print(next(gen))
print(next(gen))
print(next(gen))
# Output:
# 1
# 2
# 3

# Using Loop
def count():
    yield 1
    yield 2
    yield 3
for num in count():
    print(num)
# Output:
# 1
# 2
# 3




# GENERATOR VS RETURN
# Normal Function
def square_numbers():
    result = []
    for i in range(5):
        result.append(i * i)
    return result
print(square_numbers())
# Output:
# [0, 1, 4, 9, 16]

# Generator Version
def square_numbers():
    for i in range(5):
        yield i * i
for num in square_numbers():
    print(num)

# Output:
# 0
# 1
# 4
# 9
# 16

# MEMORY EFFICIENCY

# Bad:
numbers = [i for i in range(10000000)]
# Loads everything, Huge memory.

# Good:
numbers = (i for i in range(10000000))
# Loads when needed, Tiny memory.

# This is why generators are heavily used in backend systems.




# GENERATOR EXPRESSIONS
# Like List Comprehension.

# List Comprehension: 
squares = [x*x for x in range(5)]
print(squares)
# Output: [0,1,4,9,16]

# Generator Expression: 
squares = (x*x for x in range(5))
print(squares)
# Output: <generator object>

# Consume Generator
squares = (x*x for x in range(5))
for num in squares:
    print(num)
# Output:
# 0
# 1
# 4
# 9
# 16