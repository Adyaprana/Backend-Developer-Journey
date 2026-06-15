# Imagine you want a Calculator.

# Option 1: Write everything yourself.
# square_root_function()
# sin_function()
# cos_function()
# Thousands of lines.

# Option 2: Import Python's math module.
import math
print(math.sqrt(25))
# Much easier.
# WHAT IS A MODULE?
# A module is simply:
# A Python file containing code.

# Example: mymath.py
def add(a,b):
    return a+b
def multiply(a,b):
    return a*b
# This file itself is a module.

# WHAT IS A PACKAGE?
# A package is: A folder containing multiple modules.
# project/
#     utils/
#         __init__.py
#         math_utils.py
#         string_utils.py
# utils is a package.

# MODULE VS PACKAGE
# | Module                     | Package          |
# | -------------------------- | ---------------- |
# | Single .py file            | Folder           |
# | Contains functions/classes | Contains modules |
# | Easier                     | Larger projects  |

# IMPORT STATEMENT: Basic syntax:
# import module_name

# Example:
import math
print(math.sqrt(16))

# HOW IMPORT WORKS
# When Python sees:

import math

# Python:
# Looks for module
# Loads module into memory
# Makes functions available
# Then:
math.sqrt(16)
# works.


# FROM X IMPORT Y
# Instead of:
import math
print(math.sqrt(25))

# You can do:
from math import sqrt
print(sqrt(25))


# IMPORT MULTIPLE FUNCTIONS
from math import sqrt,pow

print(sqrt(16))
print(pow(2,3))


# IMPORT EVERYTHING
# from math import *

# Works, But avoid it. (Professional developers rarely use it)

# ALIASING: Rename modules.
import math as m
print(m.sqrt(25))

# STANDARD LIBRARY: Python comes with hundreds of built-in modules.
# No installation required.