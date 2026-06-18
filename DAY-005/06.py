# FIND MAX WITHOUT max()

numbers = [5,8,21,15,3]
largest = numbers[0]
for num in numbers:
    if num > largest:
        largest = num
print(largest)

# FIND MIN WITHOUT min()
numbers = [5,8,2,15,3]
smallest = numbers[0]
for num in numbers:
    if num < smallest:
        smallest = num
print(smallest)

# FIND AVERAGE WITHOUT average()
numbers = [5,8,2,15,3]
sum = 0
n = len(numbers)
for num in numbers:
    sum += num
avg = sum/n
print(avg)
