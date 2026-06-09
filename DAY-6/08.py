# ✅ Create 5 dictionaries
student = {
    "name": "Adyaprana",
    "age": 23
}
india = {
    "Odisha": "Bhubaneswar",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru"
}
animals ={
    "Cat": "Meow",
    "Dog": "Bark",
    "Cow":"Moo"
}
food ={
    "non-veg": "fish",
    "veg": "bread"
}
marks = {
    "math": 89,
    "english": 87,
    "physics": 98
}
print("--------------------------------")



# ✅ Access values
india = {
    "Odisha": "Bhubaneswar",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru"
}
print(india["Odisha"])
print(india.get("Karnataka"))
print("--------------------------------")



# ✅ Update values
animals ={
    "Cat": "Meow",
    "Dog": "Bark",
    "Cow":"Moo"
}
animals["Dog"] = "Woof"
print(animals)
animals["Lion"] = "Roar"
print(animals)
print("--------------------------------")



# ✅ Delete values
animals ={
    "Cat": "Meow",
    "Dog": "Bark",
    "Cow":"Moo",
    "Lion": "Roar"
}
del animals["Dog"]
print(animals)
animals.pop("Lion")
print(animals)
print("--------------------------------")



# ✅ Use keys()
animals ={
    "Cat": "Meow",
    "Dog": "Bark",
    "Cow":"Moo",
    "Lion": "Roar"
}
print(animals.keys())
print("--------------------------------")



# ✅ Use values()
animals ={
    "Cat": "Meow",
    "Dog": "Bark",
    "Cow":"Moo",
    "Lion": "Roar"
}
print(animals.values())
print("--------------------------------")



# ✅ Use items()
animals ={
    "Cat": "Meow",
    "Dog": "Bark",
    "Cow":"Moo",
    "Lion": "Roar"
}
print(animals.items())
print("--------------------------------")



# ✅ Nested Dictionary
animals ={
    "Cat": {
        "type": "Domestic",
        "sound": "Meaw"
    },
    "Dog": {
        "type": "Domestic/Wild",
        "sound": "Bark"
    },
    "Cow":{
        "type": "Domestic",
        "sound": "Moo"
    },
    "Lion": {
        "type": "Wild",
        "sound": "Roar"
    }
}
print(animals)
print("--------------------------------")



# ✅ Student Database
students = {
    "stu-1": {
        "name": "Adyaprana",
        "roll": "25mcac57",
        "course": "MCA",
        "grade": {"PYTHON": 89, "OS": 98, "DBMS": 90, "OOP": 97, "DEVOPS": 95}
    },
    "stu-2": {
        "name": "PRAVEEN",
        "roll": "25mcac50",
        "course": "MCA",
        "grade": {"PYTHON": 79, "OS": 69, "DBMS": 75, "OOP": 84, "DEVOPS": 88}
    },
    "stu-3": {
        "name": "VIKAS",
        "roll": "25mcac55",
        "course": "MCA",
        "grade": {"PYTHON": 81, "OS": 93, "DBMS": 60, "OOP": 87, "DEVOPS": 75}
    }
}
print(students)
print("--------------------------------")



# ✅ Employee Database
employee = {
    "emp-1": {
        "name": "david",
        "emp_id": "1001A",
        "Occupation": "Manager",
        "salary": 100000.00
    },
    "emp-2": {
        "name": "sam",
        "emp_id": "1004A",
        "Occupation": "Backend Developer",
        "salary": 10000000000.00
    },
    "emp-3": {
        "name": "quin",
        "emp_id": "1008A",
        "Occupation": "Cloud Architect",
        "salary": 10000.00
    }
}
print(employee)
print("--------------------------------")



# ✅ Dictionary Comprehension
squares = {
    i: i*i
    for i in range(6)
}
print(squares)
print("--------------------------------")



# ✅ Student Grade Book
student_grade_book = {
    "stu-1": {
        "name": "Adyaprana",
        "roll": "25mcac57",
        "course": "MCA",
        "grade": {"PYTHON": 89, "OS": 98, "DBMS": 90, "OOP": 97, "DEVOPS": 95}
    },
    "stu-2": {
        "name": "PRAVEEN",
        "roll": "25mcac50",
        "course": "MCA",
        "grade": {"PYTHON": 79, "OS": 69, "DBMS": 75, "OOP": 84, "DEVOPS": 88}
    },
    "stu-3": {
        "name": "VIKAS",
        "roll": "25mcac55",
        "course": "MCA",
        "grade": {"PYTHON": 81, "OS": 93, "DBMS": 60, "OOP": 87, "DEVOPS": 75}
    }
}
print(student_grade_book)
print("--------------------------------")



# ✅ Word Frequency Counter
text = input("enter a text to count: ")
words = text.split()
frequency = {}

for word in words:
    if word in frequency:
        frequency[word] += 1
    else:
        frequency[word] = 1
print(frequency)
print("--------------------------------")
