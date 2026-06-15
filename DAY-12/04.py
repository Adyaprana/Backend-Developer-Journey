# MODULE 3 — DATETIME
# Backend developers use this daily.
import datetime

# Current Date
import datetime
print(datetime.date.today())

# Current DateTime
import datetime
print(datetime.datetime.now())

# Real Backend Example
# user_created_at
# post_created_at
# payment_date
# All use datetime.





# MODULE 4 — OS
# Used heavily in backend.
import os

# Current Directory
print(os.getcwd())

# Create Folder
try:
    os.mkdir("DAY-12/test")
except:
    print("its already exit")

# # List Files
print(os.listdir())



# MODULE 5 — SYS
# Interacts with Python runtime.
import sys

# Python Version
print(sys.version)

# Arguments
print(sys.argv)