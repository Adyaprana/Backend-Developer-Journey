# RAISE: --> Create custom exceptions.
# Syntax: --> raise Exception("message")

# Example:
age = -5
if age < 0:
    raise ValueError("Age cannot be negative")

# Example: 
salary = -1000
if salary < 0:
    raise ValueError("Salary cannot be negative")

# Why Use raise: To enforce business rules, Backend uses it constantly.

amount = 0
if amount <= 0:
    raise ValueError(
        "Payment amount must be greater than zero"
    )

