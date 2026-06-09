# Dictionary Comprehension --> Short way of creating dictionaries.

# Normal Way
squares = {}

for i in range(5):
    squares[i] = i*i

print(squares)


# Pythonic Way
squares = {
    i: i*i
    for i in range(5)
}

print(squares)