# Instance Variables
# Stored separately for each object, Each object has its own copy.

class Student:

    def __init__(self, name):

        self.name = name

s1 = Student("Adyaprana")
s2 = Student("sycron")

print(s1.name)
print(s2.name)


# Class Variables
# Shared by all objects, Shared by everyone.

class Student:
    school = "KJU"
    def __init__(self,name):
        self.name = name

s1 = Student("Adyaprana")
s2 = Student("Rahul")

print(s1.school)
print(s1.name)
print(s2.school)
print(s1.name)

# Difference
# Instance Variable
# self.name
# Unique per object.

# Class Variable
# school
# Shared by all objects.