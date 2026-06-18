# Parameters --> Parameters allow data to enter a function.

def greet(name):
    print("Hello", name)

greet("Adyaprana")
print("-----------------------------------------------------------------")


def student(name, age):
    print(f"The name of student is {name} and he/she is {age} years old.")

student("Adyaprana", 23)
print("------------------------------------------------------------------")



# Real Backend Example
def create_user(username, email):

    print(username)
    print(email)
# This is exactly how backend APIs receive data.
print("------------------------------------------------------------------")



def add(a, b):
    print(f"Addition of {a}+{b}={a+b}")

add(6, 7)
print("------------------------------------------------------------------")



# Return Values: -->One of the most important concepts.
# Many beginners confuse:( print() with return )

# Print Version
def add(a, b):
    print(a + b)
add(10,20)
# Shows result. Cannot reuse result.

# Return Version
def add(a, b):
    return a + b
result = add(10,20)
print(result)
print("------------------------------------------------------------------")



# Why Return Matters --> Backend APIs return data.
def get_user():

    return {
        "name":"Adyaprana"
    }
print("------------------------------------------------------------------")


def square(n):
    return n*n
print(square(5))