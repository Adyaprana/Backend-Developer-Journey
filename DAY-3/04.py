# Nested IF statement
# we can use nested if statement when we have more than two conditions 'IF inside IF'.

age = 20

if age >= 18:

    if age >= 21:
        print("Can Drink")

    else:
        print("Adult")


username = "admin"
password = "1234"

if username == "admin":

    if password == "1234":
        print("Login Successful")

    else:
        print("Wrong Password")

else:
    print("Wrong Username")