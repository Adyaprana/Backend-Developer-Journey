# PRACTICAL 1 — JSONPLACEHOLDER API

# Use: https://jsonplaceholder.typicode.com
# Free API for testing.

# GET POSTS
# Open: https://jsonplaceholder.typicode.com/posts
# You'll receive JSON.

# GET USER
# Open: https://jsonplaceholder.typicode.com/users/1
# Response: 
{
  "id":1,
  "name":"Leanne Graham"
}

# POST REQUEST
# Use Postman or Thunder Client.
# URL: https://jsonplaceholder.typicode.com/todos
# Method: POST
# Body: 
{
  "title":"Learn FastAPI",
  "completed":False
}

# Response: 
{
  "id":201,
  "title":"Learn FastAPI"
}

# PYTHON CODE — GET REQUEST
# Install: pip install requests
# Full Working Code:
import requests
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)
print("Status Code:", response.status_code)
print(response.json())

# Output: 
# Status Code: 200
# {'userId': 1, 'id': 1, 'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit', 
#  'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'}


# PYTHON CODE — GET USER
import requests
url = "https://jsonplaceholder.typicode.com/users/1"
response = requests.get(url)
data = response.json()
print(data["name"])
print(data["email"])
print(data["phone"])
# Output: 
# Leanne Graham
# Sincere@april.biz
# 1-770-736-8031 x56442


# PYTHON CODE — POST REQUEST
import requests
url = "https://jsonplaceholder.typicode.com/todos"
payload = {
    "title": "Learn FastAPI",
    "completed": False
}
response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
# Output: 
# 201
# {'title': 'Learn FastAPI', 'completed': False, 'id': 201}
