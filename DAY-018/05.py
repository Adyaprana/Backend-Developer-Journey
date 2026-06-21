# Execution Time Decorator:

import time
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Execution Time:", end - start)
        return result
    return wrapper
@timer
def slow_function():
    time.sleep(2)
slow_function()
# O/P : Execution Time: 2.0007896423339844


# Login Logger Decorator: 
def logger(func):
    def wrapper(*args, **kwargs):
        print("User Accessed Function")
        return func(*args, **kwargs)
    return wrapper
@logger
def login():
    print("Login Success")
login()


# functools.wraps: Used in production decorators.

from functools import wraps

# Preserves function metadata.
# You'll see this in real codebases.

# Multiple Decorators: 
@auth
@logger
def profile():
    pass



# INTERVIEW QUESTIONS: 

# Q1. What is a decorator?
# Answer: A function that extends another function's behavior without modifying its source code.

# Q2. Why are decorators used?
# Answer: To add reusable functionality like: Logging, Authentication, Validation, Caching.

# Q3. What does @ symbol mean?
# Answer: Decorator syntax, Shortcut for wrapping a function.

# Q4. What are first-class functions?
# Answer: Functions that can be assigned, passed, and returned.

# Q5. Can a function return another function?
# Answer: Yes.

# Q6. Can a function accept another function?
# Answer: Yes.

# Q7. What is a closure?
# Answer: A function that remembers variables from its enclosing scope.

# Q8. Difference between decorator and closure?
# Answer: Closure stores state || Decorator modifies behavior.
# Decorators are built using closures.

# Q9. What is @staticmethod?
# Answer: Method that doesn't require self or class.

# Q10. What is @classmethod?
# Answer: Method that receives class reference (cls).

# Q11. What is @property?
# Answer: Allows method to be accessed like an attribute.

# Q12. Why are decorators important in FastAPI?
# Answer: Routes are created using decorators.
# Example:
# @app.get("/")
# @app.post("/login")

# Q13. What problem do decorators solve?
# Answer: Avoid code duplication.

# Q14. What are *args and **kwargs used for in decorators?
# Answer: To support any function signature.

# Q15. Give real-world uses of decorators.
# Answer: Logging, Authentication, Timing, Rate Limiting, Validation, API Routes.