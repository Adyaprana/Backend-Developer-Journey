# MAP() --> applies a function to every element.
print("--------------map-----------------")
# Without map
numbers = [1,2,3,4]
result = []
for n in numbers:
    result.append(n * 2)
print(result)


# Using map
numbers = [1,2,3,4]
result = map(lambda x: x * 2, numbers)
print(list(result))


# Square Numbers:
numbers = [2,4,6,8]
result = map(lambda x: x*x, numbers)
print(list(result))


# Uppercase Strings:
text = ["let's","study","python"]
result = list(
    map(str.upper,text)
)
print(list(result))


# lowercase Strings:
text = ["HELLO", "ADYAPRANA","HOW IS YOUR DAY"]
result= list(
    map(str.lower,text)
)
print(list(result))


# Add 100
prices = [100,200,300]
new_prices = list(
    map(lambda p: p + 100, prices)
)
print(new_prices)


# Backend Use Case
# Suppose API returns:
users = [
    {"name":"Adya"},
    {"name":"Rahul"}
]
# Extract names:
names = list(
    map(lambda user: user["name"], users)
)
print(names)
