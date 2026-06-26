# THEORY 6 — JSON (Most important backend data format)
# JSON = JavaScript Object Notation
# Internet's favorite data format.

# Simple JSON
{
  "name": "Adyaprana",
  "age": 23
}
# Object: Uses --> {}
{
  "name": "Adyaprana",
  "age": 23
}
# Python Equivalent
{
    "name": "Adyaprana",
    "age": 23
}
# Almost identical --> That's why Python backend developers love JSON.
# Looks exactly like dictionary.


# JSON ARRAY: Uses --> []
[
  {
    "id":1
  },
  {
    "id":2
  }
]
# Python: 
[
    {"id":1},
    {"id":2}
]

# NESTED JSON: 
# Very common.
{
  "user": {
    "name": "Adyaprana",
    "address": {
      "city": "Bangalore"
    }
  }
}

# Access mentally: data["user"]["address"]["city"]


