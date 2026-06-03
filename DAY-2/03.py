# This is the third file of the second day of the Backend Developer Journey. In this file, we will learn about the input() function and how to take user input in Python.
# input() function — take user input

name = input("Enter your name:")
age = int(input("Enter your age:"))
city = str(input("Enter your city name:"))
cgpa = float(input("Enter your cgpa:"))
is_stu = bool(input("Enter true if you are student or false:"))
print("-------------------------------------")

# print the values
print("Your name is:",name)
print("Your age is:", age)
print("You stay at:",city)
print("Your cgpa is:",cgpa)
print("You are a student:",is_stu)

print("-------------------------------------")

# Know the data's types
print("datatype of name is:", type(name))
print("datatype of age is:", type(age))
print("datatype of city is:", type(city))
print("datatype of cgpa is:", type(cgpa))
print("datatype of is_stu is:", type(is_stu))
