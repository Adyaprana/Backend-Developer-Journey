# init Method

# Purpose: Runs automatically when object is created.
# Example: 

class Student:
    def __init__(self):
        print("Student Created, Runs automatically when object is created.")

s1 = Student()


# Why init Exists

# Without it:
# Every object starts empty.

# With it:
# We can initialize data immediately.


# self Parameter

# Example: 
class Student:
    def __init__(self, name):
        self.name = name

s1 = Student("Adyaprana")

# What happens?
# self.name = "Adyaprana"
# The object stores its own name.

# Example:
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = Student("Adyaprana",23)

print(s1.name)
print(s1.age)

# self = current object
# Always remember this.