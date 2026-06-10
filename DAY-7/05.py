# REVISION CHALLENGE


# Even Odd Checker
num = int(input("Enter a number to find: "))
if num % 2 ==0:
    print("Even")
else:
    print("Odd")




# Grade Calculator
percentage = int(input("Enter your percentage to calculate your grade: "))
if percentage >= 90:
    print("A")
elif percentage >= 80:
    print("B")
elif percentage >= 70:
    print("C")
elif percentage >= 60:
    print("D")
elif percentage >= 50:
    print("E")
elif percentage >= 40:
    print("Pass")
else:
    print("Fail")




# FizzBuzz
number = int(input("Enter a number: "))
if number%3==0 and number%5 ==0:
    print("FizzBuzz")
elif number%3 == 0:
    print("Fizz")
elif number%5 ==0:
    print("Buzz")
else:
    print("invalid number")




# Multiplication Table
number = int(input("Enter a number for Multiplication Table: "))
for i in range(1,11):
    mul = number*i
    print(f"{number} x {i} = {mul}")    




# Prime Checker
number = int(input("Enter a number: "))
is_prime = True
for i in range(2,number):
    if number%i ==0:
        is_prime = False
        break
if is_prime:
    print("Prime")
else:
    print("Not prime")




# Todo App
tasks = []
while True:
    print("\n1.Add task")
    print("2.Display task")
    print("3.Removed task")
    print("4.Exit")
    choice = (input("Enter your choice: "))
    if choice == "1":
        task = input("enter what to add: ")
        tasks.append(task)
    elif choice == "2":
        print(tasks)
    elif choice == "3":
        task = input("enter what to removed: ")
        if task in tasks:
            tasks.remove(task)
    elif choice=="4":
        break
    else:
        print("invalid")
    



# Student Grade Book
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