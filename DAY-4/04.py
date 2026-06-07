# NESTED LOOPS  --> Loop inside another loop.
# for i in range():
#     for j in range():
#         code

for i in range(3):
    for j in range(3):
        print("*", end=" ")
    print()
print("------------------------------")

# Pattern Programs
# Square
for i in range(5):
    for j in range(5):
        print("*", end=" ")
    print()
print("------------------------------")

# Triangle
for i in range(1,6):
    for j in range(i):
        print("*", end=" ")
    print()