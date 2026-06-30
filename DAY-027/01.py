# THEORY 1 — MUTABLE VS IMMUTABLE

# What is Mutable: A mutable object can be changed after it is created.
# Examples: list, dict, set
# Example:
numbers = [1, 2, 3]
numbers.append(4)
print(numbers)
# Output: [1, 2, 3, 4]
# The original object changed.



# What is Immutable: Cannot be changed after creation.
# Examples: int, float, str, tuple, bool
# Example:
name = "Python"
name = name + " Backend"
print(name)
# Output: Python Backend
# The original string was not modified, A completely new string was created.

# Easy Way To Remember
# Imagine:
# Mutable --> Whiteboard (You can erase)
# Immutable --> Printed Book (Cannot modify)

# Interview Question

# What is Mutable?
# Answer: Mutable objects can be modified after creation.
# Examples: List, Dictionary, Set, 

# What is Immutable?
# Answer: Immutable objects cannot be modified after creation.
# Examples: String, Tuple, Integer, Boolean

