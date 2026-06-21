# CLOSURES: A function that remembers variables from its enclosing scope after that scope has exited.
# Example: 
def outer(message):
    def inner():
        print(message)
    return inner
hello = outer("Hello")
hello()
# Output: Hello

# Why does inner() remember message?
# Because of Closure: A closure remembers variables from its outer scope even after the outer function has finished execution.


# FIRST DECORATOR

# Normal Function: 
def greet():
    print("Hello")

# Decorator: 
def decorator_function(original_function):
    def wrapper():
        print("Before Function")
        original_function()
        print("After Function")

    return wrapper
decorated = decorator_function(greet)
decorated()

# Output: 
# Before Function
# Hello
# After Function


# Visual Flow
# greet()
#      ↓
# decorator_function()

#      ↓
# wrapper()

#      ↓
# Before
# Hello
# After


# @ DECORATOR SYNTAX: 

# Python shortcut.
# Instead of:
greet = decorator_function(greet)

# Use:
@decorator_function
def greet():
    print("Hello")
greet()

# Output
# Before Function
# Hello
# After Function


# This Is How FastAPI Works
# When you see:
# @app.get("/")
# def home():
#     return {"message": "Hello"}

# Python is actually doing something similar to:
# home = app.get("/")(home)
