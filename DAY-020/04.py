# Student Management System: 
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
    def display(self):
        print(f"Name: {self.name}")
        print(f"Marks: {self.marks}")
s1 = Student("Adyaprana", 95)
s1.display()
print("---------------------------------")





# Bank Account System: 
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        self.balance -= amount
    def show_balance(self):
        print(self.balance)
account = BankAccount(1000)
account.deposit(500)
account.withdraw(200)
account.show_balance()
print("---------------------------------")






# Employee Inheritance System: 
class Employee:
    def __init__(self, name):
        self.name = name
    def work(self):
        print("Employee Working")
class Developer(Employee):
    def code(self):
        print("Writing Python Code")
dev = Developer("Adyaprana")
dev.work()
dev.code()
print("---------------------------------")