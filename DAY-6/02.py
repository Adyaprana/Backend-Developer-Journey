# Dict: create, access, update, delete, .keys(), .values(), .items()
# Dictionary is a mutable collection of key-value pairs.


# Create Dictionary
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
print(student)


# Accessing Dictionary Values
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
print(student["name"])
print(student["age"])


# get() --> Safer method.
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
print(student.get("name"))
print(student.get("age"))

# If key doesn't exist:
print(student.get("salary"))

# Output:
# None

# Why Backend Developers Use get()
# Because API data may not always contain every key.



# Updating Dictionary

student = {
    "name": "Adyaprana",
    "age": 23
}

student["age"] = 24
print(student)

# Adding New Key

student["city"] = "Bangalore"
print(student)


# Delete Key

student = {
    "name": "Adyaprana",
    "age": 23,
    "city": "Bangalore"
}
del student["city"]
print(student)

# Alternative --> using pop
student.pop("age")
print(student)


print("----------------------------")
# Practice
# create
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
# access
print(student)
print(student["name"])
print(student.get("age"))

# update 
student["age"] = 24
print(student.get("age"))
student["cgpa"] = 9.78
print(student)

# delete
del student["age"]
print(student)
student.pop("cgpa")
print(student)




# keys --> Identifier used to access a value. must be unique.
# keys() --> Returns all keys.

student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
print(student.keys())

# values() --> Returns all values.
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
print(student.values())

# items() --> Key-value pairs.
# Returns all items.
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
print(student.items())

# Loop Through Dictionary
student = {
    "name": "Adyaprana",
    "roll": "25mcac57",
    "age": 23,
    "course": "MCA"

}
print(student.items())

for key, values in student.items():
    print(key, values)

