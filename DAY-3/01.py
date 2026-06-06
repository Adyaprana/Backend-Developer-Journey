# IF STATEMENT
# for one condition we can use if statement.
# if condition:
    # code

age = 23
if age >=18:
    print("you are an adult")

marks = 98
if marks >= 60:
    print("passed")

salary = 100000
if salary > 50000:
    print("Good Salary")

# IF ELSE STATEMENT
# for two conditions we can use if else statement.
# if condition:
    # code
# else:
    # code

age = 16
if age >=18:
    print("you are an adult")
else:
    print("you are a miner")


number = int(input("enter a number: "))
if number % 2 == 0:
    print("it's a even number")
else:
    print("it's a odd number")


mark = int(input("enter your mark: "))
if mark >= 60:
    print("you are pass")
else:
    print("you are failed")


# ELIF STATEMENT
# for more than two conditions we can use elif statement.
# if condition:
    # code
# elif condition:
    # code
# else:
    # code

percentage = int(input("enter your percentage:"))

if percentage >=90:
    print("you got A grade")
elif percentage >=80:
    print("you got B grade")
elif percentage >=70:
    print("you got C grade")
elif percentage >=60:
    print("you got D grade")
else:
    print("you got F grade")


age = int(input("enter your age:"))
if age >= 30:
    print("you can go to a party")
elif age >= 25:
    print("you can go to a club")
elif age >= 18:
    print("you can go to driving")
elif age >= 16:
    print("you can go to a movie")
elif age >= 10:
    print("you can go to a park")
else:
    print("you can't go anywhere")


temp = 35
if temp >=40:
    print("it's a very hot day")
elif temp >=30:
    print("it's a hot day")
elif temp >=20:
    print("it's a nice day")
elif temp >=10:
    print("it's a cold day")
else:
    print("it's a very cold day")