# What is a Set?
# A Set stores unique values. No duplicates allowed.

# Example
numbers = {1,2,3,3,3,4}
print(numbers)
print("----------------------")
# Output:
# {1,2,3,4} 
# Duplicates removed automatically.

# Why Use Sets?

# Fast searching.
# Removing duplicates.
# Backend validation.



# Set Operations

# Assume:
A = {1,2,3,4}
B = {3,4,5,6}
print(A)
print(B)

# Output:
# {1, 2, 3, 4}
# {3, 4, 5, 6}


# Union --> Combine all.
print(A | B)

# Output:
# {1,2,3,4,5,6}


# Intersection --> Common elements.
print(A & B)

# Output:
# {3,4}



# Difference --> Unique values.
print(A - B)

# Output: 
# {1,2}



# Remove duplicates from list using set

numbers = [1,2,2,3,3,4]
unique = list(set(numbers))
print(unique)
