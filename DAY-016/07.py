# Create Animal → Dog
class Animal:
    def eat(self):
        print("Animal is eating")
class Dog(Animal):
    pass
dog = Dog()
dog.eat()

print("-------------------------------------")






# Create Vehicle → Car
class Vehicle:
    def start(self):
        print("Vehicle Started")
class Car(Vehicle):
    pass
car = Car()
car.start()

print("-------------------------------------")






# Create Person → Student
class Person:
    def introduce(self):
        print("I am a Person")
class Student(Person):
    pass
s1 = Student()
s1.introduce()

print("-------------------------------------")






# Use super()
class Animal:
    def __init__(self,name):
        self.name = name

class Dog(Animal):
    def __init__(self,name):
        super().__init__(name)
    # pass
dog = Dog("Tommy")
print(dog.name)

print("-------------------------------------")






# Override methods
class Person:
    def introduce(self):
        print("I am a Person")
class Student(Person):
    def introduce(self):
        print("I am a Student")
s1 = Student()
s1.introduce()
print("-------------------------------------")






# Create Employee hierarchy
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, dept):
        super().__init__(name, salary)
        self.dept = dept
        self.team = []

mgr = Manager("Alice", 120000, "IT")
dev = Employee("Bob", 85000)
mgr.team.append(dev)

print(f"Manager: {mgr.name}, Dept: {mgr.dept}, Team Size: {len(mgr.team)}")
print(f"Employee: {dev.name}, Salary: ${dev.salary}")

print("-------------------------------------")






# Animal System
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
print("-------------------------------------")






# Multiple Inheritance Example
class Father:
    def skills(self):
        print("Driving")

class Mother:
    def talent(self):
        print("Cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skills()
c.talent()
print("-------------------------------------")






# isinstance()
class Person:
    def introduce(self):
        print("I am a Person")
class Student(Person):
    pass
s1 = Student()
s1.introduce()
print(isinstance(s1, Student))

print("-------------------------------------")






# issubclass()
class Person:
    def introduce(self):
        print("I am a Person")
class Student(Person):
    pass
s1 = Student()
s1.introduce()
print(issubclass(Student, Person))

print("-------------------------------------")






