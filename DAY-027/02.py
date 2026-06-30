# THEORY 2 — LIST vs TUPLE vs SET vs DICTIONARY

# | Feature          | List | Tuple | Set | Dictionary  |
# | ---------------- | ------ | ------ | ---- | ----------- |
# | Ordered          | ✅    | ✅     | ❌   | ✅         |
# | Mutable          | ✅    | ❌     | ✅   | ✅         |
# | Duplicate Values | ✅    | ✅     | ❌   | Values only|
# | Indexing         | ✅    | ✅     | ❌   | By key     |


# List: Use when data changes.
# Example:
tasks = ["Study", "Gym"]
print(tasks)
# Output: ['Study', 'Gym']


# Tuple: Use when data never changes.
# Example:
coordinates = (10, 20)
print(coordinates)
# Output: (10, 20)


# Set: Use when uniqueness matters.
numbers = {1, 2, 2, 3}
print(numbers)
# Output: {1, 2, 3}


# Dictionary: Store key-value pairs.
student = {
    "name":"Adyaprana",
    "age":23
}
print(student)
# Output: {'name': 'Adyaprana', 'age': 23}


