print("-------------Filter---------------")
# FILTER() --> removes unwanted data.
# Think: --> Keep only what matches condition.


# Without Filter: 
numbers = [1,2,3,4,5,6]
result = []
for n in numbers:
    if n % 2 == 0:
        result.append(n)
print(result)


# With Filter:
numbers = [1,2,3,4,5,6]
result =list(
    filter(lambda x: x%2==0,numbers)
)
print(result)


# Odd Numbers
numbers = [1,2,3,4,5]
result = list(
    filter(lambda x: x % 2 != 0, numbers)
)
print(result)


# Long Words
text = ["python", "go", "javascript"]
result = list(
    filter(lambda word: len(word) > 3, text)
)
print(result)


# Backend Example (Filter Active Users)
users = [
    {"name":"A","active":True},
    {"name":"B","active":False}
]
active_user = list(
    filter(lambda u: u["active"], users)
)
print(active_user)

