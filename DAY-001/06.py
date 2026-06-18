# This is the sixth file of the Backend Developer Journey. In this file, we will learn about type conversion in Python and how to convert one data type to another.
# Type conversion is the process of converting a value from one data type to another. In Python, we can use built-in functions like int(), float(), str(), etc. to perform type conversion.
age = "23"
print("type of age:", type(age))
age = int(age)
print("type of age after conversion:", type(age))
print(age)

salary = "5000000.50"
print("type of salary:", type(salary))
salary = float(salary)
print("type of salary after conversion:", type(salary))
print(salary)

number = 100
print("type of number:", type(number))
number = str(number)
print("type of number after conversion:", type(number))
print(number)

cgpa = 9.5
print("type of cgpa:", type(cgpa))
cgpa = int(cgpa)
print("type of cgpa after conversion:", type(cgpa))
print(cgpa)