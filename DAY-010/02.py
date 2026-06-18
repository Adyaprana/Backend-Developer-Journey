# TRY AND EXCEPT
# Basic Syntax:

# try:
#     risky_code
# except:
#     error_handling

# Example: 
try:
    number = int(input("Enter Number: "))
except:
    print("Invalid Input")

# Input: --> abc
# Output: --> Invalid Input
# No crash.

# Another Example
try:
    print(10/0)
except:
    print("Cannot divide by zero")
# Output: --> Cannot divide by zero

# Safe Integer Input
try:
    age = int(input("Enter Age: "))
    print(age)

except:
    print("Please enter valid integer")

# Safe Division:
try:
    a = int(input("enter a:" ))
    b = int(input("enter b:" ))
    print(a/b)
except:
    print("Something went wrong")