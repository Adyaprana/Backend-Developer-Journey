# GET REQUEST EXAMPLE: 
import requests
url = "https://api.github.com/users/octocat"
response = requests.get(url)
print("Status Code:", response.status_code)
data = response.json()
print("Username:", data["login"])
print("Name:", data["name"])
print("Followers:", data["followers"])
print("Public Repos:", data["public_repos"])


# # GITHUB PROFILE FETCHER: 
import requests
username = input("Enter GitHub Username: ")
url = f"https://api.github.com/users/{username}"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("\n===== GITHUB PROFILE =====")
    print("Username:", data["login"])
    print("Name:", data["name"])
    print("Followers:", data["followers"])
    print("Following:", data["following"])
    print("Public Repositories:", data["public_repos"])
    print("Profile URL:", data["html_url"])
else:
    print("User Not Found")


# Input: Adyaprana
# Output:
# Username: Adyaprana
# Followers: ...
# Public Repositories: ...
