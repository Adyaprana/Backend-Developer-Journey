# Constructors in Inheritance.

# Example: 
class Animal:
    def __init__(self,name):
        self.name = name

class Dog(Animal):
    pass

dog = Dog("Tommy")
print(dog.name)


# super() --> Used to call parent methods.

# Example: 
class Animal:
    def __init__(self,name):
        self.name = name

class Dog(Animal):
    def __init__(self,name):
        super().__init__(name)

dog = Dog("Tommy")
print(dog.name)


# Why super() Exists

# Without:
# Animal.__init__(self,name)

# With:
# super().__init__(name)

# Cleaner.
# Professional.
# Used everywhere.