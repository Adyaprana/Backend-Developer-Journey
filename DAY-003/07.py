# Membership Operators
# "py" in "python"   output - true

skills = ["Python","SQL"]

if "Python" in skills:
    print("Good")



# # Even Odd Checker
number = int(input("enter the number to check: "))
print("The number is:",number)
if number%2==0:
    print("Number is even number")
else:
    print("Number is odd")



# # ✅ Positive Negative Checker
number = int(input("enter the number to check: "))
print("The number is:",number)
if number > 0:
    print("Number is Positive")
elif number < 0:
    print("Number is Negative")
else:
    print("Number is zero")



# ✅ Largest of 2 Numbers
num1 = int(input("enter 1st number: "))
num2 = int(input("enter 2nd number: "))

print("The 1st number is:",num1)
print("The 2nd number is:",num2)

if num1 > num2:
    print("1st number is largest")
else:
    print("2nd number is largest")



# ✅ Largest of 3 Numbers
num1 = int(input("enter 1st number: "))
num2 = int(input("enter 2nd number: "))
num3 = int(input("enter 3rd number: "))
if num1 > num2 and num1 > num2:
    print("1st number is largest")
elif num2 > num1 and num2 > num3:
    print("2st number is largest")
else:
    print("3nd number is largest")



# ✅ Voting Eligibility
age = int(input("enter your age: "))
citizen = True
if age >= 18 and citizen:
    print("you are eligible to vote")
else:
    print("you are not eligible to vote")



# ✅ Login System
username = "admin"
password = "1234"
if username == "admin":
    if password == "1234":
        print("Login Successful")
    else:
        print("Wrong Password")
else:
    print("Wrong Username")

