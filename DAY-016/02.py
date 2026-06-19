# Parent and Child Classes

# Example: 
class Vehicle:
    def start(self):
        print("Vehicle Started")
class Car(Vehicle):
    pass
car = Car()
car.start()


# Example: 
class person:
    def introduce(self):
        print("I am a person.")
class Student(person):
    pass
s1 = Student()
s1.introduce()