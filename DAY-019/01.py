# ITERABLE VS ITERATOR

# Iterable: Something we can loop over.
# Examples:
numbers = [1, 2, 3, 4]
name = "Python"
student = {
    "name": "Adyaprana"
}
# All are iterable.
# Because:
for item in numbers:
    print(item)
# works.



# Iterator: An object that gives values one-by-one.

# Think:
# List = Full Movie Downloaded
# Iterator = Netflix Streaming
# Iterator doesn't load everything at once.

# HOW FOR LOOP REALLY WORKS
numbers = [10, 20, 30]
for num in numbers:
    print(num)

# Python secretly does:
numbers = [10, 20, 30]
iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))

# Output:
# 10
# 20
# 30