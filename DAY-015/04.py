# Instance Methods
# An instance method is a function defined inside a class that can modify or read the data of a specific object.

# Core Characteristics: 
# Uses self: It always takes self as its first parameter.
# Accesses Data: It can read or change instance variables using self.

class Student:

    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello {self.name}")

s1 = Student("Adyaprana") 
s1.greet()

class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello {self.name} you are {self.age} years old")

s1 = Student("Adyaprana",23) 
s1.greet()


# Class Methods: A class method is a function defined inside a class that belongs to the class itself, rather than to individual objects.
# Used for class-level operations. 

# Core Characteristics: 
# Uses @classmethod: It requires the @classmethod decorator right above it.
# Uses cls: It always takes cls (representing the class) as its first parameter instead of self.

# Decorator:
# @classmethod

# Example:
class Student:
    school = "KJC"
    @classmethod
    def get_school(cls):
        return cls.school
    
print(Student.get_school())



# Static Methods: A static method is a function defined inside a class that does not depend on the class or its objects to do its job.

# Core Characteristics: 
# Uses @staticmethod: It requires the @staticmethod decorator right above it.
# No self or cls: It does not take self or cls as its first parameter.
# No Data Access: It cannot access or modify instance variables or class variables.
# Used for utility functions.

# Example:

class Math:

    @staticmethod
    def add(a, b):

        return a + b
    
print(Math.add(5, 10))

# Quick Comparison:
# | Method Type | Uses self | Uses cls |
# | ----------- | --------- | -------- |
# | Instance    | Yes       | No       |
# | Class       | No        | Yes      |
# | Static      | No        | No       |


