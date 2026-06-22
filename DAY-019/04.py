# FIBONACCI GENERATOR: 

# Fibonacci is : 
# Rule: Current = Previous + Previous Previous
# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...

def fibonacci(limit):
    a = 0
    b = 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1
for num in fibonacci(10):
    print(num)


# ADVANCED VERSION: Infinite Fibonacci Generator

def fibonacci():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b
fib = fibonacci()
for _ in range(15):
    print(next(fib))





# enumerate() Returns index + value.
names = ["Python", "Java", "Go"]
for index, value in enumerate(names):
    print(index, value)
# Output:
# 0 Python
# 1 Java
# 2 Go


# zip() Combine iterables.
names = ["A", "B", "C"]
scores = [90, 80, 70]
for name, score in zip(names, scores):
    print(name, score)
# Output:
# A 90
# B 80
# C 70