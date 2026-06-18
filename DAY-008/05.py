# Scope (Local vs Global)

# Local Variable
def demo():

    x = 10

    print(x)

demo()
# Works.
# Outside?
# print(x)
# Error.
# Because it's a local scope.


# global Variable
x = 100
def demo():

    print(x)

demo()
print(x)
# Works everywhere Because it's in a global scope.


# Why Local Variables Are Better:

# Less bugs.
# Cleaner code.
# Used in professional projects.

# Docstrings
# Function documentation.

def add(a,b):
    """
    Adds two numbers
    """
    return a+b
print(add(5,8))

# How we run the Docstrings
help(add)
print(add.__doc__) 
# This will be output "Adds two numbers" becouse its not a command its a doc. string so it can run if we call it.


# Type Hints: --> Very important for FastAPI.
def add(a:int, b:int) -> int:

    return a+b

print(add(8, 9))


# Lambda Functions --> Small one-line functions.

square = lambda x: x*x

print(square(5))