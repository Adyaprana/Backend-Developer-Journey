# Build: Calculator that takes 2 inputs and does all operations

# Take Inputs
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number:"))

# Show the inputs
print(f"First number is: {num1}")
print(f"Second number is: {num2}")

# Perform operations
print(f"Addition of the two numbers is: {num1 +num2}")

sub = num1 -num2
print(f"Subtraction of the two numbers is: {sub}")

mul = num1 * num2
print(f"Multiplication of the two numbers is: {mul}")

div = num1 / num2
print(f"Division of the two numbers is: {div}")

print(f"Floor Division of the two numbers is: {num1 // num2}")
print(f"Modulus of the two numbers is: {num1 % num2}")
print(f"Power of the two numbers is: {num1 ** num2}")
