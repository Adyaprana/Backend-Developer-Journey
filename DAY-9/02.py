# What Is Lambda?

# Lambda = Anonymous Function
# Anonymous means: No name.


# Normal Function
def square(x):
    return x * x

print(square(5))

# Lambda Version
square = lambda x: x*x
print(square(5))



# Lambda Syntax
# lambda parameters: expression

# Example:
lambda x: x + 10

# Think:
# Input → Processing → Output

# Add 5
add_five = lambda x: x + 5
print(add_five(10))

# Multiply 
Multiply = lambda x, y: x*y
print(Multiply(3,4))

# Check Even
num = int(input("enter a number: "))
is_even = lambda num: num%2==0
print("Even",is_even(num))

# String Length
length = lambda text: len(text)
print(length("Python"))


# Use lambda when:

# ✅ Function is small
# ✅ Used only once

# ❌ Avoid for large logic
# ❌ Avoid for complex conditions