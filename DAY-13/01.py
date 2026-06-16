# PROJECT ARCHITECTURE
# Understand structure first.


# Feature 1
# Add Contact
# Input:
# Name
# Phone
# Email
# Store:
# contact = {
#     "name": name,
#     "phone": phone,
#     "email": email
# }
# Add to contact list.


# Feature 2
# View Contacts
# Loop through all contacts.

# Display:
# Name: Rahul
# Phone: 9876543210
# Email: rahul@gmail.com


# Feature 3
# Search Contact
# User enters: Rahul
# Search inside contacts.
# If found: Display contact.

# Feature 4
# Delete Contact
# User enters: Rahul
# Remove contact.

# Feature 5
# Save Contacts
# Store data into:
# contacts.json
# using JSON.

# STEP 1
# CREATE MAIN MENU
# When program starts:

# ===== CONTACT BOOK =====

# 1. Add Contact
# 2. View Contacts
# 3. Search Contact
# 4. Delete Contact
# 5. Save Contacts
# 6. Exit

# Question: How can user choose option?
# Answer: choice = input()


# STEP 2
# CREATE CONTACT STORAGE
# Think: Where will contacts live?
# Answer: contacts = []
# Empty list.
# Question:
# Why list: Because multiple contacts.
# Question: Why dictionary?
# Because each contact has fields.

# STEP 3
# CREATE add_contact()
# Think: What should function do?
# Inputs:
# name
# phone
# email

# Create:
# contact = {
#    ...
# }

# Add:
# contacts.append(...)

# Question:
# What should function return?

# Nothing.
# Just add contact.

# STEP 4
# CREATE view_contacts()
# Think.
# We need: 
# for contact in contacts:
# Loop through all contacts.

# Display:
# Name
# Phone
# Email

# Question: What if list empty?
# Show: No Contacts Found


# STEP 5
# CREATE search_contact()

# User enters: Rahul

# Loop through contacts.
# Check:
# if contact["name"] == search_name
# If found: Print details.

# If not found:
# Contact Not Found


# STEP 6
# CREATE delete_contact()
# User enters name.
# Loop.
# Find matching contact.
# Remove.
# Hint:
# contacts.remove(contact)
# Show:
# Contact Deleted


# STEP 7
# SAVE TO JSON
# This is the most important part.
# Backend developers do this daily.
# Import:
# import json

# Question:
# What is JSON?
# Example:
# [
#   {
#     "name":"Rahul",
#     "phone":"12345"
#   }
# ]
# JSON = Dictionary format used by APIs.

# STEP 8
# CREATE save_contacts()
# Open file.
# Convert contacts to JSON.
# Save.
# Research these functions:
# json.dump()
# and
# open()
# Understand.

# Question: Why save?
# Without saving:
# Program closes.
# Everything disappears.


# STEP 9
# LOAD CONTACTS
# Advanced Feature.
# When app starts:
# Read: contacts.json
# Convert back into list.
# Research: json.load()
# Professional applications always load previous data.


# STEP 10
# ERROR HANDLING
# What if file doesn't exist?
# Program crashes.
# Use:
# try:
# and
# except:

# Think: If file exists → load

# Else → create empty list
# PROJECT FLOW
# START
# Load Contacts

# Show Menu
#  1 Add
# 2 View
# 3 Search
# 4 Delete
# 5 Save
# 6 Exit
# Repeat Until Exit

# WHAT CONCEPTS ARE BEING USED?

# Variables
# name
# phone

# Strings
# "Rahul"

# Lists
# contacts = []

# Dictionaries
# contact = {}

# Loops
# for
# while

# Functions
# def add_contact()

# Files
# open()
# JSON json.dump()

# Error Handling
# try
# except

# INTERVIEW QUESTIONS

# Q1. Why use a list of dictionaries?
# Answer: Because we need multiple records and each record contains multiple fields.

# Q2. Why not use multiple lists?
# Answer: Difficult to manage and maintain.

# Q3. What is JSON?
# Answer: JavaScript Object Notation.
# A lightweight data exchange format.

# Q4. Why save data to JSON?
# Answer: To persist data after program closes.

# Q5. Difference between json.dump() and json.load()?
# Answer: dump() Writes Python data to JSON.
#         load() Reads JSON into Python.

# Q6. Why use functions?
# Answer: Code reuse, readability, maintainability.

# Q7. Why use try-except?
# Answer: Prevent program crashes.

# Q8. What data structure is most important in this project?
# Answer: List of Dictionaries.

# Q9. How would a database replace JSON later?
# Answer: Contacts would be stored in PostgreSQL instead of contacts.json.

# Q10. Why is this project important for backend?
# Answer: Because it mimics CRUD operations:
# Create
# Read
# Update
# Delete