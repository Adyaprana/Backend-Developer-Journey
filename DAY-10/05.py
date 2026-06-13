# ENHANCED CALCULATOR PROJECT
# # Basic Version: 
try:
    num1 = float(input("Enter Number 1: "))
    num2 = float(input("Enter Number 2: "))

    print("Addition =", num1 + num2)
    print("Subtraction  =", num1 - num2)
    print("Multiplication  =", num1 * num2)
    print("Division  =", num1 / num2)

except ValueError:

    print("Please enter valid numbers")

except ZeroDivisionError:

    print("Cannot divide by zero")


# Professional Version: 
try:
    num1 = float(input("Enter Number 1: "))
    num2 = float(input("Enter Number 2: "))

    operation  = input("Enter your action('+','-','*','/'): ")

    if  operation == "+":
        print(f"{num1} + {num2} = {num1+num2}")
    elif  operation == "-":
        print(f"{num1} - {num2} = {num1-num2}")
    elif  operation == "*":
        print(f"{num1} * {num2} = {num1*num2}")
    elif  operation == "/":
        print(f"{num1} / {num2} = {num1/num2}")
    else: 
        raise ValueError("Invalid Operations")
    
except ValueError as e:
    print("Error: ",e)
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("Calculator Closed")