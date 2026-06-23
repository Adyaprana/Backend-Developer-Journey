# Encapsulation --> One of the four pillars of OOP.
# Meaning: Hide internal implementation (Protect data) 

# Example: 
class BankAccount:
    def __init__(self):
        self.__balance = 1000
    def get_balance(self):
        return self.__balance
account = BankAccount()
print(account.get_balance())
# Output: 1000
# Trying: print(account.__balance) --> Fails.

# Why Encapsulation Matters
# Used in:
# Banking apps
# User authentication
# Payment systems
# Sensitive data should not be directly accessible.






# Inheritance: --> Inheritance allows child classes to reuse parent class code.
# Example: 
class Animal:
    def speak(self):
        print("Animal Sound")
class Dog(Animal):
    pass
dog = Dog()
dog.speak()
# Output: Animal Sound

# Real Life Example
# Animal
#  ├── Dog
#  ├── Cat
#  └── Lion

# Example: 
class Vehicle:
    def start(self):
        print("Vehicle Started")
class Car(Vehicle):
    def drive(self):
        print("Driving Car")
car = Car()
car.start()
car.drive()
# Output:
# Vehicle Started
# Driving Car





# Polymorphism: --> One interface But Different behavior.
# Example: 
class Dog:
    def sound(self):
        print("Bark")
class Cat:
    def sound(self):
        print("Meow")
animals = [Dog(), Cat()]
for animal in animals:
    animal.sound()
# Output: 
# Bark
# Meow
# Same method: sound() but Different behavior.

# Why Polymorphism Matters:
# Backend frameworks use this heavily.
# Examples:
# Database drivers
# API clients
# Authentication systems








# Abstraction: --> Hide complexity, Show only essentials.
# Example: When you drive a car: Press Accelerator You don't need engine details.
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side
sq = Square(5)
print(sq.area())
# Output: 25



# ALL 4 OOP PILLARS:

# | Pillar        | Meaning                            |
# | ------------- | ---------------------------------- |
# | Encapsulation | Hide data                          |
# | Inheritance   | Reuse code                         |
# | Polymorphism  | Same interface, different behavior |
# | Abstraction   | Hide complexity                    |
