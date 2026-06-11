# Everything in backend development is built using functions:

# FastAPI endpoints
# Database operations
# Authentication systems
# Payment processing
# API integrations
# Almost everything is a function.



# Day 8 covers:

# def
# Parameters
# Return Values
# Default Arguments
# Keyword Arguments
# *args
# **kwargs
# Scope (Local vs Global)
# Refactor Week 1 programs using functions



# BIG IDEA OF FUNCTIONS
# Imagine a restaurant.

# Without functions:
# take_order()
# cook_food()
# serve_food()
# written again and again. It's Very bad.

# Functions allow:
def take_order():
    pass

def cook_food():
    pass

def serve_food():
    pass
# Write once. and Use forever.




# Creating Your First Function
def greet():
    print("Hello Adyaprana")

# Function created. But NOT executed.
# Calling Function
def greet():
    print("Hello Adyaprana")

greet()
# Output: Hello Adyaprana



# Why Functions Matter
# Without function:
print("Welcome")
print("Welcome")
print("Welcome")

# With function:
def welcome():
    print("Welcome")
welcome()
welcome()
welcome()

def say_python():
    print("Python Backend Developer")

say_python()