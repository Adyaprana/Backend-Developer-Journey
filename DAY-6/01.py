# DICTIONARIES --> A mutable collection of key-value pairs.

# Real backend systems rarely use only lists.
# When you call an API, you usually get data like:
{
    "name": "Adyaprana",
    "age": 23,
    "city": "Bangalore"
}
# This is a Dictionary.
# Almost every API response, JSON response, database record,
# user profile, JWT token, configuration file, and backend application uses dictionaries. 
# The roadmap correctly emphasizes nested dictionaries because they're very common in API responses.

# What is a Dictionary?
# A Dictionary stores data as:
# KEY : VALUE
# Think about a student ID card:

# Name → Adyaprana
# Age → 23
# City → Bangalore

student = {
    "name": "Adyaprana",
    "age": 23,
    "city": "Bangalore"
}

# Why Dictionaries Exist

# List:
data = ["Adyaprana", 23, "Bangalore"]

# Problem:
data[1]

# What is index 1?
# Hard to understand.

# Dictionary:

student["age"]
# Much clearer.