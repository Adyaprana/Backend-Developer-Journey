# What Is Functional Programming?

# Functional Programming means:
# Instead of repeatedly writing loops,
# we use functions to transform data.

# DAY 9 MISSION — LAMBDA, MAP, FILTER, ZIP & SORTED
# Today you'll learn a style of Python called Functional Programming.
# beginners write code like this:

numbers = [1,2,3,4,5]
result = []
for n in numbers:
    result.append(n * 2)
print(result)
# Professional Python developers often write:

numbers = [1,2,3,4,5]
result = list(map(lambda x: x * 2, numbers))
print(result)

# Same result.
# Less code.
# More Pythonic.

# Your roadmap Day 9 covers:


# ✅ Understand Functional Programming
# ✅ Create Lambda Functions
# ✅ Use map()
# ✅ Use filter()
# ✅ Use zip()
# ✅ Use sorted()
# ✅ Solve 10 One-Liner Problems
# ✅ Understand where these are used in backend
# ✅ Answer interview questions