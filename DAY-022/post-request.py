import requests

data = {
    "name": "Adyaprana",
    "role": "Backend Developer"
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=data
)

print(response.status_code)

print(response.json())

# OutPut: 

# 201
# {'name': 'Adyaprana', 'role': 'Backend Developer', 'id': 101}
