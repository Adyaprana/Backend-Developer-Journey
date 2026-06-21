# FUNCTIONS ARE FIRST-CLASS OBJECTS: 

# What Does First-Class Mean?

# Functions can:
# ✅ Be stored in variables
# ✅ Be passed to functions
# ✅ Be returned from functions
# Just like integers or strings.

# Example: 
def greet():
    print("Hello")
say_hi = greet
say_hi()

# Notice: We didn't call greet()
# We stored the function inside another variable.

# Functions Inside Data Structures
def add():
    print("Add")
def subtract():
    print("Subtract")
operations = [add, subtract]
operations[0]()


# Functions are first-class objects because they can be assigned, passed, and returned like any other object.


# FUNCTIONS AS ARGUMENTS: 

# Example: 
def greet():
    print("Hello")
def execute(func):
    func()
execute(greet)

# Output: Hello

# Flow:
# greet function
#         ↓
# execute()
#         ↓
# func()
#         ↓
# Hello



# FUNCTIONS RETURNING FUNCTIONS: 

def outer():
    def inner():
        print("Inside Inner")
    return inner

result = outer()

result()

# Why Is This Important: Because decorators are built on this idea.