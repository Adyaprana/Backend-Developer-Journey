
# Create iterator from list
numbers = [10, 20, 30]
iterator = iter(numbers)
print(iterator)
print("---------------------------")






# Use next()
numbers = [10, 20, 30]
iterator = iter(numbers)
print(next(iterator))
print(next(iterator))
print(next(iterator))
print("---------------------------")






# Handle StopIteration
numbers = [10, 20, 30]
iterator = iter(numbers)
try:
    while True:
        print(next(iterator))
except StopIteration:
    print("Itreter stoped")
print("---------------------------")






# Create simple generator
def count():
    yield 1
    yield 2
    yield 3
for num in count():
    print(num)
print("---------------------------")






# Generator for squares
def square_numbers():
    for i in range(5):
        yield i * i
for num in square_numbers():
    print(num)
print("---------------------------")






# Generator for even numbers
def even_number():
    for i in range(10):
        if i%2 == 0:
            yield i
for num in even_number():
    print(num)
print("---------------------------")






# Generator expression
squares = (x*x for x in range(5))
print(squares)
print("---------------------------")






# zip() practice
names = ["A", "B", "C"]
scores = [90, 80, 70]
for name, score in zip(names, scores):
    print(name, score)
print("---------------------------")






# Fibonacci Generator
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
print("---------------------------")






# Infinite Fibonacci Generator
def fibonacci():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b
fib = fibonacci()
for _ in range(15):
    print(next(fib))
print("---------------------------")






# Prime Number Generator
def prime_generator(limit):
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            yield num
for prime in prime_generator(50):
    print(prime)