# WHILE LOOP (Used when iterations are unknown.)
# Used when we don't know how many times loop should run.
# while condition:
    # code

num = 1
while num <= 5:
    print(num)
    num += 1
print("-------------------------")
# Infinite Loop (Loop that never stops.)
# while True:
#     print("hlo")

# Print 10–1
num = 10
while num >= 1:
    print(num)
    num -= 1
print("-------------------------")


# BREAK (Stops loop completely)
for i in range(10):
    if i == 5:
        break
    print(i)
print("-------------------------")

password = "python"
while True:
    user = input("Enter Password: ")
    if user == password:
        print("Access Granted")
        break
print("-------------------------")

# CONTINUE (skips current iteration.)
for i in range(10):
    if i == 5:
        continue
    print(i)
print("-------------------------")

# Print only odd numbers.
for i in range(1, 11):
    if i %2 ==0:
        continue
    print(i)