# What Happens When You Open Instagram?

# You click (instagram.com)
# Your phone sends a request.
# Backend receives request.
# Backend checks:

# Who are you?
# Are you logged in?
# What posts should be shown?

# Then backend sends data.
# Example:
{
  "username":"adyaprana",
  "followers":500,
  "posts":120
}
# That backend is built using:

# Python
# FastAPI
# Database
# APIs
#------------------------------------------#



# HOW DAYS 1-6 CONNECT TO BACKEND

# Day 1 — Variables
# Backend stores:
username = "Adyaprana"
followers = 500
is_verified = False
# Without variables, backend cannot store data.
#------------------------------------------#

# Day 2 — Strings
# Every API uses strings.
email = "user@gmail.com"
city = "Bangalore"
password = "secret123"
# Backend handles millions of strings daily.
#------------------------------------------#

# Day 3 — Conditions
# Login systems use conditions.
saved_password = "24drt*&^"
if password == saved_password:
    print("Login Successful")
else:
    print("Enter correct password")
# Every website uses this.
#------------------------------------------#

# Day 4 — Loops
# Backend processes thousands of records.
for user in users:
    send_notification(user)
# Without loops impossible.
#------------------------------------------#

# Day 5 — Lists
# Instagram posts:
posts = [
    "Post 1",
    "Post 2",
    "Post 3"
]
# Lists store collections.
#------------------------------------------#

# Day 6 — Dictionaries
# API Response:
{
    "name":"Adyaprana",
    "age":23
}
# This is literally a dictionary.
#------------------------------------------#


# MOST IMPORTANT BACKEND CONCEPT (Data Flow)

# Frontend:
# User enters email
#      ↓
# Backend receives
#      ↓
# Validates
#      ↓
# Database stores
#      ↓
# Response sent
#      ↓
# Frontend shows result

# #------------------------------------------#
