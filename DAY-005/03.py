# LIST COMPREHENSIONS (List Comprehension is a compact way of creating lists.)

# Normal Way
squares = []
for i in range(5):
    squares.append(i*i)
print(squares)

# Pythonic Way
squares = [i*i for i in range(5)]
print(squares)

# Even Numbers 
evens = [i for i in range(20) if i % 2 == 0]
print(evens)

# Odd Numbers
odds = [i for i in range(20) if i%2!=0]
print(odds)

# String Manipulation
fruits = ["apple", "banana", "cherry"]
upper_fruits = [fruit.upper() for fruit in fruits]
