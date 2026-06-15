# CREATE YOUR OWN MODULE
# Step 1: calculator.py

# def add(a,b):
#     return a+b
# def subtract(a,b):
#     return a-b
# def multiplication(a,b):
#     return a*b
# def division(a,b):
#     return a/b
# def module(a,b):
#     return a%b
# def power(a,b):
#     return a**b

# Step 2: main.py
import calculator
print(calculator.add(10,5))


# BETTER IMPORT
from calculator import add
print(add(10,25))