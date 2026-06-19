# Method Overriding --> Child replaces parent behavior.

# Example: 
class Animal:
    def sound(self):
        print("Animal Sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

dog = Dog()
dog.sound()

# O/P --> Bark (Parent method overridden)


# Example: 
class Bird:
    def move(self):
        print("Bird Moving")

class Eagle(Bird):
    def move(self):
        print("Eagle Flying")

eagle = Eagle()
eagle.move()





# EXTRA TOPICS: 
class Animal:
    def sound(self):
        print("Animal Sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

dog = Dog()
dog.sound()

# isinstance()
print(isinstance(dog, Dog)) # Check object type.

# issubclass()
print(issubclass(Dog, Animal))