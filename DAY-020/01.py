# Why OOP Exists: 

# Imagine Instagram.
# Without OOP:
user1_name = "Adyaprana"
user1_followers = 100

user2_name = "Rahul"
user2_followers = 50

user3_name = "Amit"
user3_followers = 200
# Messy.

# Using OOP:
class User:
    pass
# Create unlimited users.
user1 = User()
user2 = User()
user3 = User()
# This is why OOP exists, To model real-world entities.



# Class: A Class is a blueprint.
# Think:
# Class = House Blueprint
# Object = Actual House
# Example
class Student:
    pass
# This creates a blueprint, No actual student yet.




# Object: Object is an instance of a class.
# Example:
class Student:
    pass
s1 = Student()
s2 = Student()
# Now actual objects exist.


# Example: 
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
s1 = Student("Adyaprana", 23)
print(s1.name)
print(s1.age)

# Output: 
# Adyaprana
# 23


