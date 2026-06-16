# Mini-Project Day — CLI App
# Build a complete CLI (command-line) Contact Book app

# Features: Add contact, view all, search by name, delete, save to JSON file
# Use functions, error handling, file I/O, dicts — everything from Week 1–2
# This is your first real project — do it 100% yourself

import json

contacts = []

def add_contact():
    contact = {}
    contact['name'] = input("Enter your name: ")
    try:
        contact['number'] = int(input("Enter the number: "))
    except ValueError:
        print("Please enter numbers only")
        return
    contact['email'] = input("Enter the email id :")

    contacts.append(contact)
    print("Contact Added")
    
def view_contacts():
    for contact in contacts:
        print(contact)
    


def search_contact():
    found = False
    search = input("Enter what you want to search: ")
    for contact in contacts:
        if contact["name"] == search:
            print(contact)
            found = True   
    if not found:
        print("Not Found")

def delete_contact():
    found = False
    search = input("Enter what you want to delete: ")
    for contact in contacts:
        if contact["name"] == search:
            contacts.remove(contact)
            print("Contact Deleted")
            print(contact)
            found = True   
    if not found:
        print("Not Found")

    
def save_contacts():
    with open("DAY-13/contacts.json", "w") as file:
        json.dump(contacts, file)
    print("Contact saved successfully!")
    try:
        with open("DAY-13/contacts.json") as file:
            data = json.load(file)      
            print(data)
    except FileNotFoundError:
        print("File not found")


print("----------------------------")
print("======= CONTACT BOOK =======")
print("----------------------------")
while True:
    print("\n")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Save Contacts")
    print("6. Exit")
    try:
        choice = (input("Enter choice: "))
    except ValueError:
        print("Please enter a valid number")
        continue

    if choice == "1":
        add_contact()
    elif choice == "2":
        view_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        save_contacts()
    elif choice == "6":
        print("== Contact Book Closed==")
        break


