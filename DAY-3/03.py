# Logical Operators
# Logical operators are used to combine conditional statements. They return a boolean value (True or False) based on the conditions provided.
# or, and, not
# Operator                                    Description
# and (Logical AND)                          Returns True if both operands are true
# or (Logical OR)                            Returns True if at least one of the operands is true
# not (Logical NOT)                          Returns True if the operand is false
# Example:

# Logical AND
# Both must be True. If one is False, the result is False.
age = 25
citizen = True
print("age is: ", age)
print("citizen is: ", citizen)
if age >= 18 and citizen:
    print("You are eligible to vote")
else:
    print("You are not eligible to vote")


# Logical OR
# One must be True. If both are False, the result is False.
marks = 80
if marks >= 90 or marks >= 75:
    print("Scholarship Eligible")


# Logical NOT
# It negates the value. If the value is True,it returns False and vice versa.
is_raining = False
if not is_raining:
    print("You can go outside")

    

num1 = 5
num2 = 3
print("num1 is: ", num1)
print("num2 is: ", num2)
print("is num1 greater than 0 and num2 greater than 0?", num1 > 0 and num2 > 0)
print("is num1 greater than 0 or num2 greater than 0?", num1 > 0 or num2 > 0)
print("is num1 not greater than 0?", not num1 > 0)
