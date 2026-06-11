# Convert Grade Calculator Into Function

# def calculate_grade(marks):
#     if marks>=100:
#         return "invalid number enter 1-100"
#     elif marks >= 90:
#         return"A"
#     elif marks >= 80:
#         return"B"
#     elif marks >= 70:
#         return"C"
#     elif marks >= 60:
#         return"D"
#     elif marks >= 50:
#         return"E"
#     elif marks >= 40:
#         return"Pass"
#     else:
#         return "Fail"
    

# percentage = int(input("Enter your percentage to calculate your grade: "))
# print(calculate_grade(percentage))

# print(calculate_grade(99))





# Calculator Using Functions

def add(a, b):
    return a+b
def sub(a,b):
    return(a-b)
def mul(a, b):
    return a*b
def div(a,b):
    return(a/b)
def add(a, b):
    return a+b
def mod(a,b):
    return(a%b)
def paw(a, b):
    return a**b

print(add(4,5))
print(sub(4,5))


# Prime Checker Function.

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num):
        if num %i ==0:
            return False
    return True
number = int(input("Enter a number to check: "))
print(is_prime(number))


