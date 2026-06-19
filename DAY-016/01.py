# INHERITANCE: How one class can reuse another class's code.

# Imagine:
# Animal
#  ├── Dog
#  ├── Cat
#  └── Lion

# All animals:
# Eat
# Sleep
# Breathe

# Inheritance lets child classes reuse parent code.

# Real World Example
# Parent: Animal

# Children:
# Dog
# Cat
# Bird

# Dog is an Animal.
# Cat is an Animal.
# Bird is an Animal.

# This relationship is called: IS-A Relationship
# Dog IS-A Animal.

class Animal:

    def eat(self):
        print("Animal is eating")

    def sleep(self):
        print("Animal is sleeping")

class Dog(Animal):    
    pass
dog = Dog()

dog.eat()
dog.sleep()
# (Animal): This means Dog inherits Animal.
# Dog automatically gets parent methods.

# Without inheritance:
# Dog
# eat() 
   
# Cat
# eat()

# Bird
# eat()
# Repeated code.

# With inheritance:
# Write once & Reuse everywhere.