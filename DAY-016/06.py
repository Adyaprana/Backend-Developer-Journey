# Build: Animal → Dog, Cat classes.
class Animal:
    def eat(self):
        print("Animal is eating")
    def sleep(self):
        print("Animal is sleeping")

class Dog(Animal):
    def sound(self):
        print("Dog is Bark")

class Cat(Animal):
    def sound(self):
        print("Cat is Meow")

dog = Dog()
dog.eat()
dog.sleep()
dog.sound()

Cat = Cat()
Cat.eat()
Cat.sleep()
Cat.sound()

# Better Version: 
class Animal:
    def __init__(self,name):
        self.name = name
    def eat(self):
        print(f"{self.name} is eating")

class Dog(Animal):
    def bark(self):
        print("Woof")

dog = Dog("Tommy")
dog.eat()
dog.bark()




# Employee → Manager → Developer
class Employee:
    def __init__(self,name,salary):
        self.name = name
        self.salary = salary
    def display(self):
        print(self.name,self.salary)

class Manager(Employee):
    def manage(self):
        print("Managing Team")

class Developer(Employee):
    def code(self):
        print("Writing Code")

dev = Developer("Adyaprana", 1000000)
dev.display()
dev.code()



# INTERVIEW QUESTIONS: 

# Q1. What is Inheritance?
# Answer: Inheritance allows one class to acquire properties and methods from another class.

# Q2. What is Parent Class?
# Answer: The class being inherited from.
# Also called: Base Class or Superclass

# Q3. What is Child Class?
# Answer: Class that inherits from another class.
# Also called: Derived Class or Subclass

# Q4. Why use Inheritance?
# Answer: Code reuse, Avoid duplication, Improve maintainability.

# Q5. What is super()?
# Answer: Used to call parent class methods and constructors.

# Q6. What is Method Overriding?
# Answer: Child class provides its own implementation of a parent method.

# Q7. Can Child Access Parent Methods?
# Answer: Yes, Directly.

# Q8. Can Parent Access Child Methods?
# Answer: No.

# Q9. What is Multiple Inheritance?
# Answer: A class inheriting from multiple parent classes.

# Q10. Does Python Support Multiple Inheritance?
# Answer: Yes.

# Q11. What is IS-A Relationship?
# Answer: Inheritance relationship.
# Example: Dog IS-A Animal

# Q12. What is isinstance()?
# Answer: Checks whether object belongs to class.

# Q13. What is issubclass()?
# Answer: Checks whether class inherits another class.

# Q14. What is MRO?
# Answer: Method Resolution Order.
# Python's lookup path for methods.

# Q15. Difference Between Composition and Inheritance?
# Answer:   Inheritance: Dog IS-A Animal
#           Composition: Car HAS-A Engine