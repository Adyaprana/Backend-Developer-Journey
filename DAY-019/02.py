# iter() --> Creates iterator.
# Example: 
numbers = [10, 20, 30]
iterator = iter(numbers)
print(iterator)
# Output: <list_iterator object>



# next() --> Gets next value.
# Example: 
numbers = [10, 20, 30]
iterator = iter(numbers)
print(next(iterator))
print(next(iterator))
print(next(iterator))

# Output:
# 10
# 20
# 30



# StopIteration Error --> After values finish:
# print(next(iterator))
# Error: StopIteration

# Example:
numbers = [1, 2, 3]
iterator = iter(numbers)
try:
    while True:
        print(next(iterator))
except StopIteration:
    print("Iterator Finished")
# Output:
# 1
# 2
# 3
# Iterator Finished



# iter() AND next()

# Every iterator has:
# __iter__() and __next__()
# These are special methods.

# Example: 
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.current > self.limit:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

counter = Counter(5)
for num in counter:
    print(num)

# Output:
# 1
# 2
# 3
# 4
# 5



# Understanding The Logic
# iter() --> Returns iterator object.
def __iter__(self):
    return self

# next() --> Returns next value.
def __next__(self):
    pass
# When finished: raise StopIteration
