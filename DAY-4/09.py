# # ✅ Print 1–100
for k in range(1,101):
    print(k)
print("---------------------------------")


# # ✅ Print even numbers
num = int(input("enter a number: "))
for i in range(num):
    if i % 2 == 0:
        print(i)
print("---------------------------------")


# # ✅ Print odd numbers
num = int(input("enter a number: "))
for i in range(num):
    if i % 2 != 0:
        print(i)
print("---------------------------------")


# ✅ Sum 1–100
sum = 0
for i in range(1, 101):
    sum = i+sum
print("sum of 1-100 is: ",sum)
print("---------------------------------")


# # # ✅ Factorial
num = int(input("enter a number for count Factorial: "))
Factorial = 1
for i in range(1, num+1):
    Factorial = i*Factorial
print(Factorial)
print("---------------------------------")


# ✅ Multiplication Table
num = int(input("enter a number for Multiplication Table: "))
for i in range(1, 11):
    mul = num*i
    print(f"{num} x {i} = ",mul)
print("---------------------------------")


# ✅ Reverse String
text = str(input("enter a string to reverse: "))
reversed_text = text[::-1]
print(reversed_text)
print("---------------------------------")


# ✅ Count vowels
text = str(input("enter a string to Count vowels: "))
vowels = "aeiouAEIOU"
count = 0
for ch in text:
    if ch in vowels:
        count += 1
print(count)
print("---------------------------------")

# # ✅ Prime Checker
number = int(input("enter a number: "))
is_prime = True
for i in range(2, number):
    if number % 2 == 0:
        is_prime = False
        break
if is_prime:
    print("its prime number")
else:
    print("not a prime number")
print("---------------------------------")

# ✅ Print primes 1–100
for num in range(2, 101):
    is_prime = True
    for i in range(2, num):
        if num % 2 == 0:
            is_prime = False
            break
    if is_prime:
        print(num)
print("---------------------------------")


# ✅ Password Checker
password = "python"
user = str(input("enter your password: "))
if password == user:
    print("valid password")
else:
    print("invalid password")
print("---------------------------------")


# ✅ Star Square Pattern
for i in range(5):
    for j in range(5):
        print("*", end=" ")
    print()
print("---------------------------------")


# ✅ Star Triangle Pattern
for i in range(1, 6):
    for j in range(i):
        print("*", end=" ")
    print()
print("---------------------------------")


# ✅ Number Triangle Pattern
for i in range(1, 6):
    for j in range(i):
        print(i, end=" ")
    print()
print("---------------------------------")
