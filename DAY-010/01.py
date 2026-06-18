# A beginner writes:

num = int(input("Enter Number: "))
print(100 / num)

# If user enters: abc
# Program crashes.
# Professional developers never allow programs to crash.
# They handle errors gracefully.
# That is why Error Handling exists.


# Exception --> Exception = Runtime Error

# Examples: (Division By Zero)
print(10 / 0)
# Output: --> ZeroDivisionError

# Invalid Integer
age = int("hello")
# Output: --> ValueError

# Wrong Index
numbers = [1,2,3]
print(numbers[10])
# Output: --> IndexError

# Missing Dictionary Key
student = {
    "name":"Adya"
}
print(student["age"])
# Output: --> KeyError

# Why Exceptions Matter

# Imagine: Instagram crashes because one user enters invalid data.
# Not acceptable.

# Instead:
# Show meaningful message
# Continue application

# That is Error Handling.