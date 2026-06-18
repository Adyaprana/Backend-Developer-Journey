# Create a BankAccount class with deposit, withdraw, balance methods

class BankAccount():

    def __init__(self, owner, balence):
        self.owner = owner
        self.balance = balence
    
    def deposit(self, amount):
        self.balance += amount

    def withdrow(self, amount):
        self.balance -= amount 
    
    def show_balance(self):
        print(self.balance)

user1 = BankAccount("sudeep",1000) 
user1.show_balance()

user1.deposit(500) 
user1.show_balance()

user1.withdrow(200) 
user1.show_balance()
print("--------------------------------")


class BankAccount():

    def __init__(self, owner, balence):
        self.owner = owner
        self.balance = balence
    
    def deposit(self, amount):
        self.balance += amount
        print(f"--Deposited money is {amount}--")

    def withdrow(self, amount):
        self.balance -= amount
        print(f"--withdrow money is {amount}--")
    
    def show_balance(self):
        print(f"Current Balence is {self.balance}")

user1 = BankAccount("sudeep",1000) 
user1.show_balance()

user1.deposit(500) 
user1.show_balance()

user1.withdrow(200) 
user1.show_balance()