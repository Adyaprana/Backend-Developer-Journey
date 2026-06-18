# JSON
# JSON means: --> JavaScript Object Notation
# Internet language --> APIs use JSON.

# Example JSON: 
{
  "name":"Adyaprana",
  "age":23,
  "city":"Bangalore"
}
# Python Dictionary: 
{
  "name":"Adyaprana",
  "age":23,
  "city":"Bangalore"
}
# Almost same.

# Why JSON Matters -->Every API returns JSON.
# Example: --> Instagram API
{
  "username":"adyaprana",
  "followers":500
}
# Backend sends JSON.
# Frontend receives JSON.

# json.dump()
# Save Python → JSON File
import json
student = {
    "name":"Adyaprana",
    "age":23
}
with open("DAY-11/student.json","w") as file:
    json.dump(student,file,indent=4)

# json.load()
# Load JSON → Python
import json
with open("DAY-11/student.json") as file:
    data = json.load(file)
print(data)