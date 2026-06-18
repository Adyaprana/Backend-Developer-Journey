print("--------------zip----------------")
# ZIP() --> combines multiple lists

# Without zip()
names = ["Adya","Rahul","Amit"]
marks = [90,85,95]
result = list(zip(names, marks))
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

# Convert Zip To Dictionary
names = ["Adya","Rahul"]
marks = [90,95]
student = dict(zip(names, marks))
print(student)

# Backend Use Case (API)
users = ["A","B","C"]
ids = [101,102,103]
customer = dict(zip(users, ids))
print(customer)
