# SPECIFIC EXCEPTIONS: (Never use generic except everywhere)
# Common exceptions: ValueError, TypeError, KeyError, IndexError, FileNotFoundError

# Example: 
# Bad: --> except:
# Good: --> except ValueError:

# ValueError --> Occurs when conversion fails.
try:
    age = int("hello")
except ValueError:
    print("Value Error Occurred")

# ZeroDivisionError:
try:
    print(10/0)
except ZeroDivisionError:
    print("Cannot divide by zero")

# COMMON EXCEPTIONS: 
# ValueError --> Wrong value.
int("abc")

# TypeError --> Wrong datatype operation.
"5" + 5

# KeyError --> Dictionary key missing.
student["salary"]

# IndexError --> List index missing.
numbers[10]

# FileNotFoundError --> File does not exist.
open("xyz.txt")

# NameError --> Variable doesn't exist.
print(age)

# AttributeError --> Wrong method.
5.upper()

# Practice Program:
try:
    numbers = [1,2,3]
    print(numbers[10])
except IndexError:
    print("Index not found")

# Multiple Exceptions: 
try:
    num = int(input("Number: "))
    print(100/num)
except ValueError:
    print("Enter valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
print("-------------------------------------------------")




# ELSE BLOCK --> Runs only if NO exception occurs.
# Why use else? --> Keeps success code separate from error code.
# Syntax:
# try:
#     code
# except:
#     code
# else:
#     code

# Example: 
try:
    age = int(input("Age: "))
except ValueError:
    print("Invalid Input")
else:
    print("Valid Input")
print("-------------------------------------------------")





# FINALLY BLOCK --> Runs ALWAYS (Whether error occurs or not)
# Syntax:
# try:
#     code
# except:
#     code
# finally:
#     code

# Example: 
try:
    num = int(input("Enter a number: "))
    print(10/num)
except ZeroDivisionError:
    print("Error")
finally:
    print("Program Finished")


# Real Backend Example ( Database Connection)
# try:
#     connect_database()
# except:
#     print("DB Error")
# finally:
#     close_database()

