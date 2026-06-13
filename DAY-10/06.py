# Exception Object
try:
    int("abc")
except ValueError as error:
    print(error)
# Output: invalid literal for int()


# Catch Multiple Exceptions Together
try:
    n = 10
    m = int(input("enter a number: "))
    print(n/m)

except (ValueError, TypeError, ZeroDivisionError):

    print("Handled")

# Exception Hierarchy: 
# All exceptions inherit from: 
Exception
# Example:
try:
    n = 10
    m = int(input("enter a number: "))
    print(n/m)
except Exception as e:
    print(e)


# THEORY
# How Backend APIs Use Error Handling

# Imagine:
# User Registration API
# User enters:
# {
#   "email":"wrong-email"
# }
# Backend:
# raise ValueError("Invalid Email Format")

# API returns:
# {
#     "error":"Invalid Email Format"
# }

# Instead of crashing.
# This is exactly why FastAPI and Django use exception handling everywhere.




# INTERVIEW QUESTIONS

# Q1. What is an Exception?
# Answer: An error that occurs during program execution.

# Q2. Why use Error Handling?
# Answer: To prevent application crashes and handle errors gracefully.

# Q3. What does try do?
# Answer: Contains code that may raise an exception.

# Q4. What does except do?
# Answer: Handles the exception.

# Q5. What does else do?
# Answer: Runs when no exception occurs.

# Q6. What does finally do?
# Answer: Always executes whether exception occurs or not.

# Q7. Difference between Exception and Error?
# Answer: Exceptions can be handled, Errors usually indicate serious problems.

# Q8. What is ValueError?
# Answer: Occurs when value type conversion fails, --> Example: int("abc")

# Q9. What is TypeError?
# Answer. Occurs when incompatible datatypes are used.

# Q10. What is KeyError?
# Answer: Occurs when dictionary key doesn't exist.

# Q11. What is IndexError?
# Answer: Occurs when list index is out of range.

# Q12. What is FileNotFoundError?
# Answer: Occurs when requested file doesn't exist.

# Q13. What is raise?
# Answer: Used to manually generate exceptions.

# Q14. Why use custom exceptions?
# Answer: To enforce business rules and validate data.

# Q15. What is except ValueError as e?
# Answer: Captures exception object for detailed error messages.