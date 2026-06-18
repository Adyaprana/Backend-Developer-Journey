# What Is A Loop?
# A loop repeatedly executes a block of code.

# Without loop:
print("Hello")
print("Hello")
print("Hello")
print("Hello")
print("Hello")

print("---------------------")

# With loop:
for i in range(5):
    print("Hello")
print("---------------------")

# FOR LOOP: (Used when number of iterations is known.)
# for variable in sequence:
#     code

for i in range(5):
    print("Adyaprana")
print("---------------------")

for i in range(5):
    print(i)
print("---------------------")

# range() -->Generates sequence of numbers.
# range(start, stop, step)

for i in range(1, 6):
    print(i)
print("---------------------")

for i in range(2, 11, 2):
    print(i)
print("---------------------")

# Print 1–10
for i in range(1, 11):
    print(i)
print("---------------------")

# Print Even Numbers
for i in range(2, 21, 2):
    print(i)