# Multiplication Table 

number = int(input("enter the number:"))
print(f"The Multiplication Table for {number} is:")
for i in range(1, 11):
    mul = number*i
    print(f"{number} x {i} = {mul}")


print("--------------------------------------------")

num = int(input("Enter Number: "))
for i in range(1,11):
    print(f"{num} x {i} = {num*i}")
