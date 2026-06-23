# Constructor (init) --> Constructor runs automatically when object is created.
# Example:
class Car:
    def __init__(self):
        print("Car Created")
c1 = Car()
# Output: Car Created

# Why Constructor Matters
# Used for:
# Initial values
# Database connections
# API clients
# Configuration loading
# Very common in backend development. 




# Instance Variables: --> Each object gets its own data.
# Example:
class Student:
    def __init__(self, name):
        self.name = name
s1 = Student("Adyaprana")
s2 = Student("Rahul")
print(s1.name)
print(s2.name)
# Output:
# Adyaprana
# Rahul




# Methods: --> Functions inside classes.
# Example:
class Student:
    def greet(self):
        print("Hello Student")
s1 = Student()
s1.greet() 
# Output: Hello Student

# Example:
class Student:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print(f"Hello {self.name}")
s1 = Student("Adyaprana")
s1.greet()
# Output: Hello Adyaprana