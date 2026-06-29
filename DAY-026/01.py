# THEORY 1 — WHAT IS AN API?
# Imagine a restaurant.
# You          = Client
# Waiter       = API
# Kitchen      = Server

# You ask: Give me Burger -> API takes request -> Kitchen prepares -> API returns response.
# Exactly same thing happens in software.




# THEORY 2 — WHAT IS REQUESTS?
# Requests is Python's most popular HTTP library.
# Install: pip install requests
# Verify:
import requests
print("Installed Successfully")




# THEORY 3 — WHAT IS HTTP?
# Whenever you open: https://github.com
# your browser sends:
# GET / HTTP/1.1
# to GitHub -> The server responds -> This communication uses HTTP.

# HTTP METHODS:
# Most important: GET, POST, PUT, PATCH, DELETE.
# For now learn: GET, POST.




# THEORY 4 — GET REQUEST
# GET means: Give me data
# Example:
import requests
response = requests.get(
    "https://api.github.com/users/octocat"
)
print(response.status_code)
# Output: 200

# STATUS CODES:
# 200 = Success
# 201 = Created
# 400 = Bad Request
# 401 = Unauthorized
# 403 = Forbidden
# 404 = Not Found
# 500 = Server Error




# THEORY 5 — RESPONSE OBJECT
# Requests returns a Response object.
import requests
response = requests.get(
    "https://api.github.com/users/octocat"
)
print(type(response))
# Output: <class 'requests.models.Response'>




# THEORY 6 — .text
# Returns raw response.
import requests
response = requests.get(
    "https://api.github.com/users/octocat"
)
print(response.text)
# Large JSON output appears.





# THEORY 7 — .json()
# Converts JSON into Python dictionary.
import requests
response = requests.get(
    "https://api.github.com/users/octocat"
)
data = response.json()
print(data)
# Output:
# {
#    "login":"octocat",
#    ...
# }

# Access Data
import requests
response = requests.get(
    "https://api.github.com/users/octocat"
)
data = response.json()
print(data["login"])
# Output: octocat




# THEORY 8 — HEADERS
# Headers contain metadata.
import requests
response = requests.get(
    "https://api.github.com/users/octocat"
)
print(response.headers)
# Output:
# {
#  'content-type':'application/json'
# }

# Example
import requests
response = requests.get(
    "https://api.github.com/users/octocat"
)
print(response.headers["Content-Type"])
# Output: application/json





# THEORY 9 — POST REQUEST
# POST means: Send Data
# Example:
import requests
payload = {
    "name":"Adyaprana",
    "course":"MCA"
}
response = requests.post(
    "https://httpbin.org/post",
    json=payload
)
print(response.status_code)
print(response.text)
# Output: 200

