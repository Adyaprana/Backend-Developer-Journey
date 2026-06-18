print("-----------------------------------")
# Create Student class
class student():
    def __init__(self, name):
        self.name = name

s1 = student("Adyaprana")
print(s1.name)
print("-----------------------------------")






# Create Employee class
class employee():
    def __init__(self, id):
        self.id = id
e1 = employee(10067)
print(e1.id)
print("-----------------------------------")






# Create Car class
class car():
    def __init__(self, car_name):
        self.car_name = car_name
c1 = car("BMW")
print(c1.car_name)
print("-----------------------------------")






# Create 3 objects from each
class car():
    def __init__(self, car_name):
        self.car_name = car_name

c1 = car("BMW")
c2 = car("AUDI")
c3 = car("TOYOTA")

print(c1.car_name)
print(c2.car_name)
print(c3.car_name)
print("-----------------------------------")






# Practice instance variables
class Car:
    def __init__(self, car_name, color, year):
        self.car_name = car_name
        self.color = color
        self.year = year

c1 = Car("BMW", "Black", 2024)
c2 = Car("Audi", "White", 2026)

print(f"Car 1 is a {c1.color} {c1.car_name} from {c1.year}.")
print(f"Car 2 is a {c2.color} {c2.car_name} from {c2.year}.")

print("-----------------------------------")






# Practice class variables
class Car:
    Type = "luxury" 
    def __init__(self, car_name, color, year):
        self.car_name = car_name
        self.color = color
        self.year = year
        
    @classmethod
    def get_type(cls):
        return cls.Type
    
c1 = Car("BMW", "Black", 2024)
c2 = Car("Audi", "White", 2026)

print(f"Car 1 is a {c1.color} {c1.car_name} from {c1.year} is {c1.get_type()}.")
print(f"Car 2 is a {c2.color} {c2.car_name} from {c2.year} is {c2.get_type()}.")

print("-----------------------------------")





# Practice instance methods
class Car:
    def __init__(self, car_name, color):
        self.car_name = car_name
        self.color = color

    def start_engine(self):
        return f"The {self.color} {self.car_name}'s engine is roaring!"

c1 = Car("BMW", "Black")
print(c1.start_engine())
print("-----------------------------------")






# Practice class methods
class Car:
    total_cars = 0

    def __init__(self, car_name):
        self.car_name = car_name
        Car.total_cars += 1

    @classmethod
    def get_total_count(cls):
        return f"Total cars created: {cls.total_cars}"

car1 = Car("BMW")
car2 = Car("Audi")

print(Car.get_total_count()) 
print("-----------------------------------")






# Practice static methods
class MathUtils:
    
    @staticmethod
    def add_numbers(x, y):
        return x + y

result = MathUtils.add_numbers(5, 10)
print(result)  
print("-----------------------------------")






# Build BankAccount project
class BankAccount:
    bank_name = "Global Digital Bank" 

    def __init__(self, account_holder, balance=0.0):
        self.account_holder = account_holder  
        self.balance = balance                

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New Balance: {self.balance}")
        else:
            print("Invalid deposit amount!")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. Remaining Balance: {self.balance}")
        else:
            print("Insufficient funds or invalid amount!")


print(f"Welcome to {BankAccount.bank_name}")

account = BankAccount("Adyaprana", 500.0)

account.deposit(150.0)
account.withdraw(50.0)
print("-----------------------------------")





