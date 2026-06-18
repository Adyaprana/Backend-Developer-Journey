#  Read text file
file = open("DAY-11/skills.txt")
content = file.read()
print(content)
file.close()
print("------------------------------------")





#  Write text file
file = open("DAY-11/student.txt","w")
file.write("hii python")
file = open("DAY-11/student.txt")
content = file.read()
print(content)
file.close()
print("------------------------------------")





#  Append text file
file = open("DAY-11/student.txt","a")
file.write("\nHow are you?")
file = open("DAY-11/student.txt")
content = file.read()
print(content)
file.close()
print("------------------------------------")





#  Read line by line
file = open("DAY-11/skills.txt")
content = file.readline()
print(content)
file.close()
print("------------------------------------")





#  Create CSV file
import csv
with open("DAY-11/emp.csv","w") as file:
    writer = csv.writer(file)
    writer.writerow(["id","names"])
    writer.writerow([101,"ADYAPRANA"])
    writer.writerow([121,"sukh"])
print("------------------------------------")





#  Read CSV file
import csv
with open("DAY-11/emp.csv") as file:
    read = csv.reader(file) 
    print(list(read))
print("------------------------------------")





#  Save dictionary to JSON
import json
emp  = {
    "name": "ADYAPRANA",
    "emp_id": "1002"
}
with open("DAY-11/emp.json","w") as file:
    json.dump(emp,file,indent=4)
print("------------------------------------")





#  Load JSON file
import json
with open("DAY-11/emp.json") as file:
    data = json.load(file)
    print(data)
print("------------------------------------")





#  Student Record System
import json
name = input("Enter your name: ")
age = int(input("Enter your age: "))
student = {
    "name": name,
    "age": age
}
with open("day-11/stu.json","w") as file:
    json.dump(student,file,indent=4)
with open("day-11/stu.json") as file:
    data = json.load(file)
    print(data)
print("------------------------------------")





#  Multiple Student Manager
import json
students = []
while True:
    name = input("Name: ")
    if name == "exit":
        break
    age = int(input("Age: "))
    students.append({
        "name":name,
        "age":age
    })
with open("DAY-11/stu.json","w") as file:
    json.dump(students,file,indent=4)
with open("day-11/stu.json") as file:
    data = json.load(file)
    print(data)
print("------------------------------------")





#  Contact Book using JSON
import json
contact = {"Alice": "123-456-7890"}
with open("DAY-11/contacts.json", "w") as file:
    json.dump(contact, file)
print("Contact saved successfully!")
with open("DAY-11/contacts.json") as file:
    data = json.load(file)
    print(data)
print("------------------------------------")





#  Expense Tracker using JSON
import json
expenses = [
    {"item": "Pizza", "cost": 12.50},
    {"item": "Bus Ticket", "cost": 2.00}
]
with open("DAY-11/expenses.json", "w") as file:
    json.dump(expenses, file)
print("Expenses saved successfully!")
with open("DAY-11/expenses.json") as file:
    data = json.load(file)
    print(data)
print("------------------------------------")





#  Student Database using CSV
import csv

header = ["ID", "Name", "Grade"]
student_data = ["101", "Alex", "A"]
with open("DAY-11/students.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)        
    writer.writerow(student_data)  
print("Student database created!")
with open("DAY-11/students.csv") as file:
    read = csv.reader(file) 
    print(list(read))
print("------------------------------------")




