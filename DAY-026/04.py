# Query Parameters:
# Example:
params = {
    "q": "Python"
}
requests.get(
    url,
    params=params
)
# Requests automatically builds URL.




# Timeout:
# Never do: requests.get(url)
# Better:
requests.get(
    url,
    timeout=5
)
# Prevents hanging forever.




# Error Handling:
# Professional way:

import requests
try:

    response = requests.get(
        "https://api.github.com/users/octocat",
        timeout=5
    )
    print(response.status_code)
except requests.exceptions.RequestException as e:
    print("Error:", e)




# JSON → Dictionary
# Remember: API returns:
{
  "name":"Adyaprana"
}
# Python receives:
{
  "name":"Adyaprana"
}
# This is why Dictionaries were so important earlier.


