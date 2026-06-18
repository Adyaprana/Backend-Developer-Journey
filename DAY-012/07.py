# Create your own module
def add(a,b):
    return a+b
def subtract(a,b):
    return a-b
def multiplication(a,b):
    return a*b
def division(a,b):
    return a/b
def module(a,b):
    return a%b
def power(a,b):
    return a**b
print("------------------------------------------------")






# Import your module:
import calculator
print(calculator.add(10,5))
#          OR            
from calculator import add
print(add(10,25))
print("------------------------------------------------")






# Use math module
from math import *
print(add(5,8))

print(sqrt(470))

print(pow(2,8))
print("------------------------------------------------")






# Use random module
import random
print(random.randint(1,100))

number = [1,4,7,8,9,6,3 ]
random.shuffle(number)
print(number)

dsa = ["tree", "graph","array","linked list", "stack", "queue" ]
print(random.choices(dsa))
print("------------------------------------------------")






# Use datetime module
import datetime
print(datetime.date.today())

print(datetime.datetime.now())
print("------------------------------------------------")






# Use os module
import os
print(os.getcwd())
try:
    os.mkdir("DAY-12/test")
except:
    print("its already exit")
print(os.listdir())
print("------------------------------------------------")






# Create virtual environment
# python -m venv env
print("------------------------------------------------")






# Activate it
# env\Scripts\activate
print("------------------------------------------------")






# Install requests
# pip install flask
print("------------------------------------------------")





# Generate requirements.txt
# pip freeze > requirements.txt
print("------------------------------------------------")






# Delete environment
# deactivate
# rmdir /s /q venv
print("------------------------------------------------")






# Create again
# python -m venv env
print("------------------------------------------------")






# Explain venv in your own words

#                  PYTHON VIRTUAL ENVIRONMENTS (venv)

# 1. WHAT IT IS
# ------------------------------------------------------------------------
# * A built-in Python module that creates a virtual isolation chamber 
#   for your specific projects.
# * Think of it as a separate, mini-installation of Python living inside 
#   your project folder.
# * It is completely detached from your computer's main, global Python 
#   installation.


# 2. WHY IT IS USED
# ------------------------------------------------------------------------
# * It prevents dependency conflicts between different coding projects.
# * Without venv, every project shares one giant pool of system libraries.
# * Example: If Project A needs an OLD version of a tool (e.g., v1.0) and 
#   Project B needs a NEW version (e.g., v2.0), installing the new one 
#   will overwrite and break Project A. venv keeps them safely separate.


# 3. KEY BENEFITS
# ------------------------------------------------------------------------
# * NO VERSION CONFLICTS
#   Run different versions of the same library on your computer at the 
#   same time.

# * CLEANER SYSTEM
#   Keeps your computer's global Python environment clutter-free.

# * EASY COLLABORATION
#   Generates a tiny text file (requirements.txt) so other developers 
#   can recreate your exact setup with a single command.

# * SAFE EXPERIMENTATION
#   Install, upgrade, or delete libraries without worrying about 
#   breaking your other working projects.

# * NO ADMIN PRIVILEGES NEEDED
#   Install packages freely without needing administrator or root 
#   permissions on your machine.

print("------------------------------------------------")





