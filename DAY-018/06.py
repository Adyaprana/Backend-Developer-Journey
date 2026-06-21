# Create 3 normal functions
def greet():
    print("Hello from a normal function!")
def add(a, b):
    return a + b
def square(num):
    return num * num
greet()
print(f"Add result: {add(5, 3)}")
print(f"Square result: {square(4)}")
print("--------------------------------------")






# Pass function as argument
def run_another_function(func, value):
    # This takes a function and executes it with a value
    return func(value)

result = run_another_function(square, 5)
print(f"Result from passing square function: {result}")
print("--------------------------------------")






# Return function from function
def greeting_factory(greeting_word):
    def internal_greet(name):
        print(f"{greeting_word}, {name}!")
    return internal_greet # Returning the function object
say_hola = greeting_factory("Hola")
say_hola("Amigo")
print("--------------------------------------")






# Create custom decorator
def simple_decorator(func):
    def wrapper():
        print("[Before] Something happens before the function is called.")
        func()
        print("[After] Something happens after the function is called.")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello World!")

say_hello()
print("--------------------------------------")






# Decorator with arguments
def repeat(times):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return actual_decorator
@repeat(times=3)
def cheer():
    print("Hurrah!")
cheer()
print("--------------------------------------")






# Timer decorator
import time
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.6f} seconds to run.")
        return result
    return wrapper

@timer_decorator
def slow_loop():
    total = 0
    for i in range(1000000):
        total += i
    return total

slow_loop()
print("--------------------------------------")






# Logger decorator
print("--------------------------------------")
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Running '{func.__name__}' with arguments: {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] '{func.__name__}' finished and returned: {result}")
        return result
    return wrapper

@logger_decorator
def multiply(x, y):
    return x * y

multiply(4, 5)
print("--------------------------------------")






# Authentication decorator simulation
print("--------------------------------------")
user_session = {"is_authenticated": False}

def require_auth(func):
    def wrapper(*args, **kwargs):
        if not user_session["is_authenticated"]:
            print("Access Denied: Please log in first!")
            return None
        return func(*args, **kwargs)
    return wrapper

@require_auth
def view_dashboard():
    print("Welcome to the secret dashboard!")

# 1. Try while logged out
view_dashboard()

# 2. Log in and try again
user_session["is_authenticated"] = True
view_dashboard()
print("--------------------------------------")






# Experiment with @staticmethod, @classmethod, @property
class Employee:
    company_name = "Tech Corp"  # Class variable

    def __init__(self, first_name, last_name, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary

    # Experiment with @property
    @property
    def full_name(self):
        # Allows accessing a method like a normal attribute without ()
        return f"{self.first_name} {self.last_name}"

    # Experiment with @classmethod
    @classmethod
    def change_company(cls, new_name):
        # Receives the class (cls) as an argument, not the instance (self)
        cls.company_name = new_name
        print(f"Company name updated to: {cls.company_name}")

    # Experiment with @staticmethod
    @staticmethod
    def is_work_day(day_name):
        # Behaves like a normal function inside a class namespace (no self or cls)
        work_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        return day_name.title() in work_days


# 1. Testing @property
emp = Employee("John", "Doe", 50000)
print(f"Employee Full Name: {emp.full_name}")  # Notice: No parenthesis () used!

# 2. Testing @classmethod
Employee.change_company("Global Tech Inc.")

# 3. Testing @staticmethod
print(f"Is Sunday a work day? {Employee.is_work_day('Sunday')}")
print(f"Is Monday a work day? {Employee.is_work_day('Monday')}")
print("--------------------------------------")
