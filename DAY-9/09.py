# ✅ Create 10 lambda functions

# add two numbers: 
print(list(map(lambda x,y: x+y, [4],[6])))
# Square two numbers: 
print(list(map(lambda x: x**2, [1,2,3,4,5])))
# Cube two numbers: 
print(list(map(lambda x: x**3, [1,2,3,4,5])))
# check even: 
print(list(map(lambda e: e%2==0,[1,2,3,4,5])))
# check odd: 
print(list(map(lambda e: e%2!=0,[1,2,3,4,5])))
# Combine 2 list: 
print(list(zip([1,2,3],["adyaprana","hari","ram",])))
# Uppercase: 
print(list(map(str.upper,["python","java"])))
# Lowercase: 
print(list(map(str.lower,["Python","Java"])))
# 7. Long Words:
print(list(map(lambda c: len(c)>4, ["python", "cloud","os"])))
#8. Sort Length:
print(list(sorted([3,5,2,9,7,1,5,])))
print("-------------------------------")




# ✅ Square numbers:
numbers = [2,5,8,7,9]
result = list(
    map(lambda x: x**2,numbers)
)
print(result)
print("-------------------------------")




# ✅ Cube numbers: 
numbers = [2,5,8,7,9]
result = list(
    map(lambda x: x**3,numbers)
)
print(result)
print("-------------------------------")




# ✅ Add two numbers
num1 = [5]
num2 = [7]
result = list(
    map(lambda x,y: x+y, num1,num2)
)
print(result)
print("-------------------------------")




# ✅ 5 map programs
num1 = [56]
num2 = [70]
result = list(
    map(lambda x,y: x+y, num1, num2)
)
print(result)

number = [1,2,3,4,5]
result = list(
    map(lambda x: x*2,numbers)
)
print(result)

number = [1,2,3,4,5]
result = list(
    map(lambda x: x**2, number)
)
print(result)

text = ["python","java","c++"]
result = list(
    map(str.upper,text)
)
print(result)

price = [156, 768, 978]
result = list(
    map(lambda x: x+100, price)
)
print(result)
print("-------------------------------")




# ✅ 5 filter programs
number = [1,2,3,4,5,6]
result = list(
    filter(lambda x: x%2==0,number)
)
print(result)

text = ["python", "cloud","c++","go","java"]
result = list(
    filter(lambda x: len(x)>4,text)
)
print(result)

users = [
    {"name":"A","active":True},
    {"name":"B","active":False}
]
result = list(
    filter(lambda x: x["active"], users)
)
print(result)

numbers = [1,2,3,4,5]
result = list(
    filter(lambda x: x % 2 != 0, numbers)
)
print(result)
print("-------------------------------")




# ✅ 5 zip programs
names = ["adyaprana", "david", "sam"]
age = [23,34,25]
result = list(
    zip(names,age)
)
print(result)

cities = [
    "Bangalore",
    "Delhi",
    "Mumbai"
]
states = [
    "Karnataka",
    "Delhi",
    "Maharashtra"
]
print(list(zip(cities, states)))

names = ["adyaprana", "david", "sam"]
marks = [98,87,76]
result = dict(
    zip(names,marks)
)
print(result)

users = ["A","B","C"]
ids = [101,102,103]
customer = dict(zip(users, ids))
print(customer)
print("-------------------------------")




# ✅ Student Marks Processor
# Take marks list
# Use map to add grace marks
# Use filter for passing students
# Use sorted for ranking
marks = list(map(int, input("Enter list elements separated by space: ").split()))
grace = 30
print("your marks are: ",marks)
print("the grace mark is: ",grace)
result = list(
    map(lambda x: x + grace, marks)
)
print(result)
result2 = list(
    filter(lambda x: x >= 70,result)
)
print(result2)
result3 = sorted(result2, reverse=True)
print(result3)
print("-------------------------------")




# ✅ Employee Salary Analyzer
# Filter salaries > 50000
# Sort employees
# Create dictionary using zip
names = ["alice", "bob", "david", "sam"]
salaries = [7000000, 60000, 5000,2500]

emp_data = dict(zip(names, salaries))
print(emp_data)

print("-------------------------------")



