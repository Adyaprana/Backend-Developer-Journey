# Getters and Setters: 

# Suppose: balance = -10000
# Should not happen, We need validation.

# Traditional Getter: 
class Student:
    def __init__(self):
        self.__age = 23
    def get_age(self):
        return self.__age

student = Student()
print(student.get_age())


# Traditional Setter: 
class Student:
    def __init__(self):
        self.__age = 23
    def set_age(self, age):
        if age > 0:
            self.__age = age


# Why Use Setters --> Validation.

# Example:
# student.set_age(-5)
# Rejected.




class Student:
    def __init__(self):
        self.__age = 23

    # Traditional Setter
    def set_age(self, age):
        if age > 0:
            self.__age = age

    # Traditional Getter (Needed to view the private variable)
    def get_age(self):
        return self.__age

student = Student()

# 1. Change the age using the setter
student.set_age(25)

# 2. View the age using the getter
print(student.get_age())  #  Outputs: 25
