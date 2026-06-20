# ENCAPSULATION, POLYMORPHISM

# What is Encapsulation?
# Hiding internal implementation details and controlling access to data.

# Think: ATM Machine.

# You can:
# Withdraw Money
# Check Balance
# Deposit Money

# You cannot:
# Directly modify bank database




# Public Variables: Default in Python.
class Student:
    def __init__(self):
        self.name = "Adyaprana"

# Usage:
s = Student()
print(s.name)

# Output: Adyaprana



# Protected Variables (_var)
# Convention only Single underscore.
class Student:
    def __init__(self):
        self._age = 22

# Meaning: "Please don't access this directly."
# Example:(Still possible)
s1 = Student()
print(s1._age)

# Works Output: 22




# Private Variables (__var)
# Double underscore 

class BankAccount:

    def __init__(self):
        self.__balance = 1000

account = BankAccount()
# print(account.__balance)

# Error -->AttributeError: 'BankAccount' object has no attribute '__balance'

# Why?
# Python performs: "_BankAccount__balance" internally.

# This is called:
# Name Mangling

# Example
class BankAccount:

    def __init__(self):
        self.__balance = 1000

account = BankAccount()

print(account._BankAccount__balance)

# Output: 1000
# Technically accessible but discouraged.