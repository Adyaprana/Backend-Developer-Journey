# STUDENT RECORD SYSTEM:

# Save Student
import json
name = input("Enter your name: ")
age = int(input("Enter your age: "))
student = {
    "name": name,
    "age": age
}
with open("day-11/stu.json","w") as file:
    json.dump(student,file,indent=4)

# Read Student
import json
with open("day-11/stu.json") as file:
    data = json.load(file)
    print(data)


# MULTIPLE STUDENTS SYSTEM

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