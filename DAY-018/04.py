# DECORATOR WITH ARGUMENTS

# Problem:
def greet(name):
    print(name)

# Old wrapper breaks.
# Need:
# *args
# **kwargs

# Solution
def decorator_function(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@decorator_function
def greet(name):
    print(f"Hello {name}")
greet("Adyaprana")

# Output: 
# Before
# Hello Adyaprana
# After


# COMMON DECORATOR 1
# @staticmethod: Normally methods need self.
class Math:
    def add(self, a, b):
        return a + b

# Static Method doesn't need object.
class Math:
    @staticmethod
    def add(a, b):
        return a + b
print(Math.add(5, 3))
# Output: 8


# COMMON DECORATOR 2
# @classmethod: Receives class itself.
class Student:
    school = "KJC"
    @classmethod
    def get_school(cls):
        return cls.school
print(Student.get_school())
# Output: KJC


# COMMON DECORATOR 3
# @property: Makes method behave like attribute.

# Without property:
# person.full_name()

# With property:
# person.full_name

# Example: 

class Person:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    @property
    def full_name(self):
        return f"{self.first} {self.last}"
p = Person("Adyaprana", "Pradhan")
print(p.full_name)

# Output: Adyaprana Pradhan

